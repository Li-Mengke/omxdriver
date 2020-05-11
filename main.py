import tkinter
import os
import subprocess
from omxplayer import OmxDriver
import time
import logging
from playlist import PlayList

if __name__ == '__main__':


    '''root = tkinter.Tk()
    root.attributes('-fullscreen', True)
    canvas = tkinter.Canvas(root, background = 'black', height = 1080, width = 1920)
    canvas.grid(row = 0, column = 0)
    tkinter.mainloop()'''

    # driver = OmxDriver('widget', '')
    # driver.load('/home/pi/Desktop/ADVideo/pets.mp4', '')
    # time.sleep(10)

    tracklist = os.listdir('/home/pi/Desktop/ADVideo')
    que = PlayList(maxsize = 3)
    que.populate(playlist)
    first_track = que.get()
    driver = OmxDriver('widget', '')
    driver.load(first_track)
    time.sleep(4)
    driver.pause()


    exit()