#This file

import json
import tkinter


class Background():

    def __init__(self, height = 720, width = 1080, background_color = 'black', fullscreen = True, start_position = Null):
        '''

        :param height: height of the canvas
        :param width:
        :param background:
        '''
        self.height = height
        self.width = width
        self.background_color = background_color
        self.fullscreen = fullscreen
        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.root, background=self.background_color, height=self.height, width=self.width)
        self.canvas.grid(row=0, column=0)
        tkinter.mainloop()

    def get_canvas(self, x=0, y=0):
        root = tkinter.Tk()
        canvas = tkinter.Canvas(root, background=self.background_color, height=self.height, width=self.width)
        canvas.grid(row=0, column=0)
        tkinter.mainloop()

        return canvas



class ProfileEditor()