import logging
import pika
import os

class Error_Handler():

    def __init__(self):
        logging.basicConfig(filename='/home/pi/PycharmProjects/untitled/app.log', filemode = 'a', format = '%(name)s - $(levelname)s - %(message)s')
        logging.basicConfig(level = logging.DEBUG)
        self.logger = logging.getLogger('logger')

    def
