import logging
import os



class LogManager():
    '''
    this class manages logs and write to a file in the /logging/ directory. If fatal error occurs, this also restarts the program and
    exists itself elegantly. Report terminal error to server
    '''

    def __init__(self):
        self.logger = logging.getLogger('logger')

    def