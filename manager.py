<<<<<<< HEAD
from player import Player
from playlist import PlayList
import threading
import multiprocessing
from mq_manager import MQManager
=======
from error_manager import Error_Handler
>>>>>>> 2cd9086109c87a3b75d2fda9bc228fcd77379338

handler = Error_Handler()
logger = handler.get_logger()

<<<<<<< HEAD
class Manager():

    def __init__(self, dict):
        self.dict = dict
        mq = MQManager(self.dict)
=======
logger.warning('something')
>>>>>>> 2cd9086109c87a3b75d2fda9bc228fcd77379338
