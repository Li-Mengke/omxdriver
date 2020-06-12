import pika
import yaml
import requests
import json
import os
from log_manager import Error_Handler
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

        self.MAC_Address = 'mac-123456'
        # self.MAC_Address = self.getMacAddress()
        self.queue_name = self.MAC_Address + '_queue'
        self.exchangeName = "qutou.osp-exchange"
        self.routing_key = self.MAC_Address + '-routingKey'
        self.logger = self.error_handler.get_logger()

    def monitor(self):
        #connect to MQ server, and then start monitoring. This should be called in its own thread
        credentials = pika.PlainCredentials(user_name, password)
        parameters = pika.ConnectionParameters(host = host_name, port = port, virtual_host='/', credentials = credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.basic_consume(queue = queue_name, on_message_callback = self.callback, auto_ack= True)


        #start monitoring MQ server
        channel.start_consuming()

    def callback(ch, method, properties, body):
        '''
        this method is the call back when a message from MQ is received.
        Do somgthing about the received message
        :param method:
        :param properties:
        :param body:
        :return:
        '''

        #first write to database
        try:
            conn = sqlite3.connect(r'omxdriver/db/app.db')

        raise NotImplementedError

        #then decode the message and start download
        raise NotImplementedError

        #now change file settings and restart the program
        raise NotImplementedError


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
        while attempts < 10:
            if os.path.exists(fileName):
                header = requests.head(url)
                fileLength = int(header.headers['Content-Length'])
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




with open('mqresult.txt') as f:
    data = json.load(f)

url = data['content']['putintoTask']['url']
fileName = data['content']['putintoTask']['materialName']

result = download(url, fileName)
print(result)