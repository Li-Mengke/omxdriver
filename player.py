from omxplayer import OmxDriver
from playlist import PlayList
import threading
import os
import logging
from queue import Empty

class Player():

    def __init__(self, video_dir, gapless = True):
        self.previous = None
        self.current = None
        self.next = None
        self.video_dir = video_dir
        self.track_list = os.listdir(self.video_dir)
        self.list = PlayList(caller = self, maxsize = len(self.track_list))

    def initial_load(self):
        if len(self.track_list) == 0:
            self.display_logo()
        elif len(self.track_list) == 1:
            self.current = OmxDriver('widget', '')
            self.play_loop(self.current)
        else:
            self.list.populate(self.track_list)
            self.current = OmxDriver('widget', '')
            self.next = OmxDriver('widget', '')
            self.current.load(self.get_video_path(self.video_dir, self.list.get()))
            self.next.load_and_pause(self.get_video_path(self.video_dir, self.list.get()))
            self.continuous_play()


    def continuous_play(self):
        try:
            while True:
                self.current.pause_at_end()
                self.next.unpause()
                self.previous = self.current
                self.previous.terminate('play finished')
                self.current = self.next
                # self.next = self.previous
                self.next = OmxDriver('widget', '')
                try:
                    next_track = self.list.get()
                except Empty:
                    logging.info('empty queue, re-populating')
                    self.list.populate(self.track_list)
                    next_track = self.list.get()
                self.next.load_and_pause(self.get_video_path(self.video_dir, next_track))


                #dbug info
                # print('continuous play loop finished')
                # import psutil
                # pid = os.getpid()
                # ps = psutil.Process(pid)
                # print('memory used = ' + str(ps.memory_info()))
                # import gc
                # print('object used' + str(gc.get_count()))
        except KeyboardInterrupt:
            try:
                self.previous.terminate()
                self.current.terminate()
                self.next.terminate()
            except:
                pass
            finally:
                exit(1)

    def continuous_play_single_loop(self):
        try:
            self.current.pause_at_end()
            self.next.unpause()
            self.previous = self.current
            self.previous.terminate('play finished')
            self.current = self.next
            # self.next = self.previous
            self.next = OmxDriver('widget', '')
            try:
                next_track = self.list.get()
            except Empty:
                logging.info('empty queue, re-populating')
                self.list.populate(self.track_list)
                next_track = self.list.get()
            self.next.load_and_pause(self.get_video_path(self.video_dir, next_track))
        except KeyboardInterrupt:
            try:
                self.previous.terminate()
                self.current.terminate()
                self.next.terminate()
            except:
                pass
            finally:
                exit(1)

    def get_video_path(self, video_dir, video_name):
        return video_dir + '/' + video_name

    def play_loop(self, driver):
        self.list.populate(self.track_list)
        self.current = OmxDriver('widget', '')
        try:
            self.current.load(self.get_video_path(self.video_dir, self.list.get()), ' --loop ')
        except KeyboardInterrupt:
            self.current.terminate('keyboard interruption')


    def display_logo(self):
        raise NotImplementedError
