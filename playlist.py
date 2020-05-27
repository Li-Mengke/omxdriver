import queue
import logging


class PlayList():



    def __init__(self, caller = None, maxsize = 10):
        self.player = caller
        self.queue = queue.Queue(maxsize = maxsize)


    def populate(self, list):
        print('full status ' + str(self.queue.full()))
        while not self.queue.full():
            print('notfull')
            for i in list:
                try:
                    self.queue.put(i,block =  False)
                except:
                    logging.info('queue is full, finished populating')
                    return

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
        except queue.Empty as e:
            raise e
        except:
            raise
            # qisfull = self.queue.full()
            # qisempty = self.queue.empty()
            # size = self.queue.qsize()
            # logging.error('an error occured when trying to get item from queue, queue empty is '
            #               + str(qisfull) + ' empty status is ' + str(qisempty) + 'size now is ' + str(size))

    def dump(self):
        while True:
            try:
                self.get()
            except queue.Empty:
                print('dump finished')
                break
