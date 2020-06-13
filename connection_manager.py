import pika
import yaml
import requests
import json
import os
from error_manager import Error_Handler
import sqlite3


class MQManager():
    '''this class monitors the server MQ and when message received, react.
    It also pushes data back to the server'''

    def __init__(self, dict):
        '''
        initiate the mq manager and its variables.  Mostly it loads the settings.
        this class should be unique in the running program(one instance)
        :param dict: arguments for initiating the class
        :param log_manager: log manager object for the class to use
        '''

        #read the yml settings file
        with open('application-dev.yml') as f:
            var = yaml.load(f, Loader=yaml.SafeLoader)

        #setting the variables
        self.host_name = var['rabbitmq']['host']
        self.port = var['rabbitmq']['port']
        self.user_name = var['rabbitmq']['username']
        self.password = var['rabbitmq']['password']

        self.MAC_Address = 'mac-3'
        # self.MAC_Address = self.getMacAddress()
        self.queue_name = self.MAC_Address + '-queue'
        self.exchangeName = "qutou.osp-exchange"
        self.routing_key = self.MAC_Address + '-routingKey'
        self.error_handler = Error_Handler('MQ_handler')

    def monitor(self):
        #connect to MQ server, and then start monitoring. This should be called in its own thread
        self.credentials = pika.PlainCredentials(self.user_name, self.password)
        self.parameters = pika.ConnectionParameters(host = self.host_name, port = self.port, virtual_host='/', credentials = self.credentials)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.basic_consume(queue = self.queue_name, on_message_callback = self.callback, auto_ack= True)


        #start monitoring MQ server
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        '''
        this method is the call back when a message from MQ is received.
        Do somgthing about the received message
        :ch
        :param method:
        :param properties:
        :param body:
        :return:
        '''
        #convert message received into a dictionary file
        data = json.loads(body.decode('utf-8'))
        print(data)

        #loop through the received messages and execute these commands
        for item in data:
            for task in item['content']:
                raise NotImplementedError



        #now change file settings and restart the program

        self.error_handler.graceful_restart()


        with open("mqresult.txt", 'a') as f:
            f.write(body.decode("utf-8"))
        print(body)


    def getMacAddress(self):
        '''
        :return: the MAC address of the machine
        '''
        import uuid
        MAC_Address = ':'.join(("%012X" % uuid.getnode())[i:i+2] for i in range(0, 12, 2))
        return MAC_Address

    def download(url, fileName):
        '''
        this method downloads a file and implements resume function by using a loop until done
        :param fileName: file-name to store the downloaded file
        :return:
        '''
        attempts = 0
        header = requests.head(url)
        fileLength = int(header.headers['Content-Length'])
        fileName ='video/'+fileName
        while attempts < 10:
            if os.path.exists(fileName):
                if fileLength == os.path.getsize(fileName):
                    return True
                else:
                    with open(fileName, 'ab') as f:
                        position = f.tell()-1024
                        pos_header = {}
                        print(position)
                        pos_header['Range'] = f'bytes={position}-'

                    with requests.get(url, headers = pos_header, stream = True) as r:
                        with open(fileName, 'ab') as f:
                                #some validation should be here

                            for chunk in r.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(r.content)
                                    f.flush()
                                    print(os.path.getsize(fileName))

            else:
                try:
                    with requests.get(url, allow_redirects=True, stream = True) as r:
                        with open(fileName, 'wb') as f:
                            iter = 0
                            for chunk in r.iter_content(chunk_size = 1024):
                                if chunk:
                                    f.write(chunk)
                                    f.flush()
                                    iter += 1
                                # if iter > 2000:
                                #     break
                except:
                    raise NotImplementedError('not yet handled')
                # except requests.exceptions.ConnectionError:
                #     self.logger.info('Connection error '+attempts+', trying again')
                # except requests.exceptions.Timeout:
                #     self.logger.info('Connection timed out on attempt '+ attempts +', trying again')
                # except requests.exceptions.TooManyRedirects as e:
                #     self.error_handler.report_issue('Too many redirects', e.print_tb(file = './log/download_log.log'))
            attempts += 1
        return False




# with open('mqresult.txt') as f:
#     data = json.load(f)
#
# url = data['content']['putintoTask']['url']
# fileName = data['content']['putintoTask']['materialName']
#
# result = download(url, fileName)
# print(result)


class USBMonitor():
    def __init__(self):
        raise NotImplementedError

    def monitor(self):
        raise NotImplementedError

    def callback(self):
        # convert message received into a dictionary
        data = json.loads(body.decode('utf-8'))
        print(data)

        # loop through the received messages and execute these commands
        for plan in data:
            for t in plan['tasks']:
                monitor = t['monitorType'].split(',')
                if '1' in monitor:
                    upMonitor = 1
                else:
                    upMonitor = 0

                if '2' in monitor:
                    dailyMonitor = 1
                else:
                    dailyMonitor = 0

                if '3' in monitor:
                    downMonitor = 1
                else:
                    downMonitor = 0

                task = Task(materialName=plan['materialName'], planId=plan['planId'], url=plan['url'],
                            upTime=t['upTime'], downTime=t['downTime'], isMonitor=t['isMonitor'],
                            upMonitor=upMonitor, dailyMonitor=dailyMonitor, downMonitor=downMonitor,
                            taskType=t['taskType'], pointId=t['pointId'], playSchedule=t['playSchedule'],
                            taskId=t['taskId'], mac=t['mac'], monitorPeriod=t['monitorPeriod'],
                            monitorRate=t['monitorRate'])

                # save loaded command into database
                db.execute("""INSERT INTO localtask VALUES(
                                      :materialName, :planId, :url, :upTime, :downTime, :isMonitor, :upMonitor, :dailyMonitor, 
                                      :downMonitor, :taskType, :taskType, :pointId, :playSchedule, :mac, :monitorPeriod, :monitorRate)
                                    """, task.getTaskDict())

                # execute task
                task.execute(self)

        # now change file settings and restart the program

        self.error_handler.graceful_restart()

        raise NotImplementedError

    def copy(self):
        raise NotImplementedError
