import tkinter
import logging

class tk_manager():

    def __init__(self):
        self.root = tkinter.Tk()
        self.logger = logging.getLogger('logger')
        return

    def run(self, dict):
        self.screen_width = self.root.winfo_screenmmwidth()
        self.screen_height = self.root.winfo_screenheight()
        print('screen size is ' + str(self.screen_height) + ' by ' + str(self.screen_width))
        self.num_screens = dict['screen_config']['num_screens']
        if self.num_screens != len(dict['screen_config'])-1:
            '''this is a fatal error, report'''
            logger.error('number of screens does not match given number of parameters')

