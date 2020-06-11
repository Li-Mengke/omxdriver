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

        self.root = tkinter.Tk()
        self.root.config(bg='black')
        self.root.attributes('-fullscreen', True)
        self.root.after(1, main)
        tkinter.mainloop()





def read_yaml(filename):
    import yaml
    '''
    loads a yml file for its contained parameters
    :param fn: file name to read
    :return: loaded result as a dictionary
    '''
    with open(filename) as f:
        result = yaml.load(f, Loader=yaml.SafeLoader)
    return result
dict = read_yaml('config.yml')
bg = tk_manager()
bg.run(dict)