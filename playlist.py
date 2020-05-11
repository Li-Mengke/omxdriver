import queue



class PlayList():
    self.queue = None
    self.player = None



    def __init__(self, caller, maxsize):
        self.player = caller
        self.queue = queue.Queue(maxsize = maxsize)


    def populate(self, list):
        while not self.queue.full():
            for i in list:
                try:
                    queue.put(i, False)
                except:
                    logging.info('queue is full, finished populating')
                    break

    def put(self, item, block = False, timeout = None):
        try:
            self.queue.put(item, block = block, timeout = None)
            return True
        except:
            logging.error('an error occured when calling queue put')
            return False

    def get(self):
        try:
            return self.queue.get(timeout = 0.01)
        except:
            qisfull = self.queue.full()
            qisempty = self.queue.empty()
            size = self.queue.qsize()
            logging.error('an error occured when trying to get item from queue, queue empty is '
                          + qisfull + ' empty status is ' + qisempty + 'size now is ' + size)
            return False




