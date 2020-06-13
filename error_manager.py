import logging
import pika
import os

class Error_Handler():

<<<<<<< HEAD
    def __init__(self, name):
        logging.basicConfig(filename='log/app.log', filemode = 'a', format = '%(name)s - $(levelname)s - %(message)s')
        logging.basicConfig(level = logging.DEBUG)
        self.logger = logging.getLogger('logger')
        self.name = name
=======
    def __init__(self):
        logging.basicConfig(filename='log/app.log', filemode = 'a', format = '%(name)s - %(asctime)s - %(levelname)s - %(message)s', level = logging.DEBUG)
>>>>>>> 2cd9086109c87a3b75d2fda9bc228fcd77379338


    def report_issue(self, message, file = None):
        raise NotImplementedError

    def graceful_restart(self):
        raise NotImplementedError

    def display_message(self, message):
        raise NotImplementedError



