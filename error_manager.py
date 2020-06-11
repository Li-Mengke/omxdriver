import logging
import pika
import os

class Error_Handler():

    def __init__(self):
        logging.basicConfig(filename='log/app.log', filemode = 'a', format = '%(name)s - %(asctime)s - %(levelname)s - %(message)s', level = logging.DEBUG)


    def report_issue(self, message, file = None):
        raise NotImplementedError



