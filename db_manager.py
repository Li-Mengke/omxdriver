import sqlite3
import os
from error_manager import Error_Handler

class LocalDB():

    def __init__(self, db_address):
        '''
        create a db manager object that connects to local task db
        :param db_address: database file address
        '''
        self.db_address = db_address
        self.error_handler = Error_Handler('db_handler')

        #if first time install and the db does not exist, create one
        if not os.path.exists(self.db_address):
            self.create_table()

    def execute(self, cmd, data = {}):
        '''
        same as sqlite3 execute, takes commands and format dictionary
        :param cmd: sql command
        :param data: data that goes with the sql command
        :return:
        '''
        try:
            #create a connection and execute command
            conn = sqlite3.connect(self.db_address)
            cur = conn.cursor()
            cur.execute(cmd, data)
            conn.commit()
        except sqlite3.Error as e:
            #catch error and let error_hander to handle it
            raise e
            # self.error_handler.report_issue('error')
            # self.error_handler.graceful_restart()
        finally:
            try:
                conn.close()
            except:
                pass

    def create_table(self):
        try:
            self.execute("""CREATE TABLE displaytask(
                                        taskType TEXT,
                                        planId INT(18),
                                        materialName VARCHAR,
                                        materialId INT,
                                        materialType TEXT,
                                        videoDuration INT,
                                        url VARCHAR(256),
                                        height INT,
                                        width INT,
                                        upTime TEXT,
                                        downTime TEXT,
                                        isMonitor INT,
                                        upMonitor INT,
                                        dailyMonitor INT,
                                        downMonitor INT,
                                        pointId INT(18),
                                        taskId INT(18),
                                        playSchedule VARCHAR(32),
                                        mac CHAR(17),
                                        monitorPeriod INT,
                                        monitorFrequency INT
                                        )
                                        """)
            self.execute("""CREATE TABLE monitortask(
                            taskType TEXT, 
                            monitorType INT,
                            monitorId INT(18),
                            pointId INT(18),
                            taskId INT(18),
                            monitorPeriod INT,
                            monitorFrequency INT
                            )""")

        except:
            raise
            # self.error_handler.report_issue('error')
            # self.error_handler.graceful_restart()

