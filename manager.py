from player import Player
from playlist import PlayList
import threading
import multiprocessing
from mq_manager import MQManager


class Manager():

    def __init__(self, dict):
        self.dict = dict
        mq = MQManager(self.dict)
