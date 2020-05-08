import tkinter
import os
import subprocess
from omxplayer import OmxDriver
import time

if __name__ == '__main__':


    '''root = tkinter.Tk()
    root.attributes('-fullscreen', True)
    canvas = tkinter.Canvas(root, background = 'black', height = 1080, width = 1920)
    canvas.grid(row = 0, column = 0)
    tkinter.mainloop()'''

    driver = OmxDriver('widget', '')
    driver.load('/home/pi/Desktop/ADVideo/pets.mp4', '')
    time.sleep(10)
    exit()