import logging
import pika
import os

class Error_Handler():

    def __init__(self):
        logging.basicConfig(filename='log/app.log', filemode = 'a', format = '%(name)s - $(levelname)s - %(message)s')
        logging.basicConfig(level = logging.DEBUG)
        self.logger = logging.getLogger('logger')

    def get_logger(self):
        return self.logger

    def report_issue(self, message, file = None):
        raise NotImplementedError



