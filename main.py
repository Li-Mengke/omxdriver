import tkinter
import os
import subprocess
from omxplayer import OmxDriver
import time
import logging
from playlist import PlayList
from player import Player
import threading
import logging

class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def exit(self, event = None):
        self.root.destroy()
        exit(1)

    def run(self):
        self.root = tkinter.Tk()
        self.root.config(bg='black')
        self.root.attributes('-fullscreen', True)
        self.root.protocol('WM_DELETE_WINDOW', self.callback)
        self.button_canvas = tkinter.Canvas(self.root, background = 'black', height = 20, width = 20)
        self.button_canvas.place(x = 1900, y = 1060)
        self.button = tkinter.Button(self.button_canvas, text = 'exit', command = self.exit)
        self.button.pack()
        self.root.bind("<Return>", self.exit)
        self.root.mainloop()

    def read_yaml(fn):
        '''
        loads a yml file for its contained parameters
        :param fn: file name to read
        :return: loaded result as a dictionary
        '''
        with open(fn) as f:
            result = yaml.load(f, Loader=yaml.SafeLoader)
        return result

if __name__ == '__main__':
    '''
    configuring logging module
    '''
    logging.basicConfig(filename='app.log', filemode='w',
                        format='%(asctime)s - %(name)s - %(thread)d - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger('logger')
    # this is a experiment for tkinter and canvas

    # root = tkinter.Tk()
    # root.attributes('-fullscreen', True)
    # screen_width = root.winfo_screenwidth()
    # screen_height = root.winfo_screenheight()
    # #root.geometry('%dx%d%+d%+d' % (screen_width, screen_height, 0, 0))
    # canvas = tkinter.Canvas(root, background = 'black', height = screen_height, width = screen_width)
    # canvas.place(x = -1, y = -1)
    # tkinter.mainloop()
    #
    # time.sleep(3)


    # this portion plays two videos in a gapless fashion

    video_dir = '/home/pi/Desktop/ADVideo'


    # #this portion is experiment on playlist implementation
    # list = PlayList(maxsize = 3)
    # list.populate(tracklist)
    # list.dump()
    # print(list.get())

    #this portion tries using player to play an infinite loop of videos gaplessly
    # root = tkinter.Tk()
    # root.config(bg='black')
    # root.attributes('-fullscreen', True)
    # canvas = tkinter.Canvas(root, width=1100, height=800, background='black')
    # canvas.place(x=0, y=0)
    # player = Player(video_dir, True)
    # player.initial_load()
    # root.after(1, player.initial_load())
    import pdb
    # pdb.set_trace()
    # root.after(1, player.continuous_play())
    # tkinter.mainloop()

    #this is tested and good to go
    app = App()
    while True:
        player = Player(video_dir, True)
        player.initial_load()





    #driver.terminate('just do it')
