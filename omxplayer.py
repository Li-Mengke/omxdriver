import dbus
import os
import sys
import signal
import subprocess
import time
import logging


class OmxDriver():

    omx_command = "omxplayer --no-keys --win '0,0,1080,720'"
    # omx_command = 'omxplayer --no-keys'

    def __init__(self, options = None):

        self.logger = logging.getLogger('OMXlogger')

        #initiate passed-in parameters

        #initiate some object status parameters
        self.started = False
        self.paused = False
        self.dbus_found = False
        self.dbus_connected = False
        self.player_running = False
        self.process_running = False

        #initiate some variables to contain pointers to subprocess and dbus controls
        self.process = None
        self.dbus_root = None
        self.dbus_props = None
        self.dbus_player = None

        #statistics
        self.duration = -1

        # get options passed in
        if options is not None:
            if 'volume' in options:
                self.volume = options['volume']

    def load(self, track, cmd_options = None, first_track = False):

        self.cmd_options = cmd_options

        #getting the user
        self.dbus_user = os.environ['USER']

        #generate a ordered id
        self.id = str(int(time.time()*100))
        self.dbus_name = "org.mpris.MediaPlayer2.omxplayer" + self.id


        #generate the command to call
        if cmd_options == None or cmd_options == '':
            self.omxplayer_cmd = OmxDriver.omx_command + " --dbus_name '" + self.dbus_name + "' " + track
        else:
            self.omxplayer_cmd = OmxDriver.omx_command + self.cmd_options + " --dbus_name '"+ self.dbus_name + "' " + track


        #start the process and get its pid
        self.process = subprocess.Popen(self.omxplayer_cmd, shell=True,stdout=open('/dev/null','a'),stderr=open('/dev/null','a'))
        self.pid = self.process.pid

        #connect to dbus
        result = self.wait_for_dbus()
        if result == False:
            self.logger.error('failed to connect to dbus after multiple attempts')
            #self.terminate('dbus connection failure')
        # else:
        #     print('dbus info is: ', self.dbus_player, self.dbus_props, self.dbus_root)

        #check and update status
        self.player_running = self.process_is_running()

        #get duration
        self.duration = self.check_duration()
        if self.duration <0:
            self.logger.error('failed to get duration of track, terminating program')
            self.terminate('failed to get duration of track')

        #if not the first track loaded, pause at the very beginning

        return result

    def load_and_pause(self, track, cmd_options = None):
        self.load(cmd_options = cmd_options, track = track)
        self.paused = False
        while self.paused == False:

            position = self.get_position()
            print(position)
            if position > -200000:
                self.pause()
                self.paused = True



    def pause_at_end(self):
        sleep_time = self.duration - self.get_position() - 500000
        time.sleep(sleep_time/1000000)
        while True:
            if self.process_is_running():
                time_till_end = self.duration - self.get_position()
                if time_till_end < 300000:
                    self.pause()
                    #print('paused successfully' + str(time_till_end))
                    break

    def pause(self):
        '''
        try to pause the current track
        :return: True or False based on success
        '''
        if self.process_is_running():
            tries = 0
            while tries <= 5:
                try:
                    self.dbus_player.Pause()
                    tries += 1
                except dbus.exceptions.DBusException as e:
                    self.logger.error('failed to pause player because of a dbus error ' + e.get_dbus_message())
                paused = self.player_is_paused()
                if paused == 'Paused':
                    self.paused = True
                    return True
                if paused == None:
                    self.logger.error('pause failed becasue failed to check pause status from dbus, assuming the program has ended')
                    return False
            return False
        else:
            self.logger.warning('trying to pause when the process is not running')


    def unpause(self):
        attempts = 0
        result = False
        while self.paused == True and attempts < 5:
            try:
                attempts += 1
                self.dbus_player.Action(16)
            except dbus.exceptions.DBusException as e:
                self.logger.error('faield to unpause because of dbus error: ' + e.get_dbus_message())
                return False
            paused = self.player_is_paused()
            if paused == 'Paused':
                self.paused = True
                self.logger.error('attemts ' + str(attempts) + ' failed to unpause the video')
                result = False
            else:
                self.paused = False
                result = True
        return result



    def check_duration(self):
        '''
        check the duration of the currently loaded track. If failed, log relavent information
        :return: length of the current track in microseconds
        '''
        micros = -1
        tries = 0
        while micros < 0 and tries <= 5:
            if self.process_is_running():
                try:
                    micros = self.dbus_props.Duration()
                except dbus.exceptions.DBusException as e:
                    self.logger.error('failed to check track duration: ' + e.get_dbus_message())
            else:
                self.logger.warning('trying to check duration when process is not running')
            tries += 1
        return micros


    def set_volume(self, millibels = 6000):
        '''
        set the volume for the player through dbus. If failes, log information
        :param millibels: volume to set in millibels
        :return: True or False indicating success
        '''
        try:
            self.dbus_props.Volume(pow(10, millibels/2000.0))
            return True
        except dbus.exceptions.DBusException as e:
            self.logger.error('failed to set volume through dbus: ' + e.get_dbus_message())
            return False


    def exit(self, reason):
        #if process is running, try exiting. Otherwise, log error
        if self.process_is_running():
            try:
                self.dbus_root.Quit()
                return True
            except dbus.exceptions.DBusException as e:
                self.logger.error('failed to exit because of a dbus error: ' + e.get_dbus_message())
                return False
        else:
            self.logger.error('the process is not runing while trying to exit')
            return False

    def terminate(self, reason):
        self.logger.warning('terminating the program, becasue: ' + reason)
        #sending quit signal to dbus
        try:
            self.dbus_root.Quit()
        except:
            return False
        return True

        #because there is a lag between signal sent and process stopping. Tune this just enough to prevent an unnecessary recursion
        sleeptime = 0.2
        time.sleep(sleeptime)
        if self.process_is_running():
            self.logger.error(f'process is still running %f s after keyboard interrupt is sent', sleeptime )
            self.terminate('failed to terminate, trying again')
        else:
            self.logger.info('process terminated')

    def process_is_running(self):
        #check the status of the player when called
        if self.process.poll() == None:
            return True
        else:
            return False

    def player_is_paused(self):
        if self.process_is_running():
            try:
                result = self.dbus_props.PlaybackStatus()
            except dbus.exceptions.DBusException as e:
                self.logger.warning('faled to check player status: ' + e.get_dbus_message())
                return None
            return result
        else:
            self.logger.warning('process is not running, cannot test player')
            return True

    def get_position(self):
        position_ms = -1
        if self.process_is_running():
            try:
                position_ms = self.dbus_props.Position()
            except dbus.exceptions.DBusException as e:
                self.logger.warning('failed to get position, running on: ' + e.get_dbus_message())
        else:
            self.logger.warning('trying to get position when process is not running')
        return position_ms

    def mute(self):
        if self.process_is_running():
            try:
                self.dbus_player.Mute()
                return True
            except dbus.exceptions.DBusException as e:
                self.logger.warning('failed to mute player: ' + e.get_dbus_message())
                return False

    def unmute(self):
        if self.process_is_running():
            try:
                self.dbus_player.Unmute()
                return True
            except dbus.exceptions.DBusException as e:
                self.logger.warning('failed to unmute player: ' + e.get_dbus_message())
                return False

    def wait_for_dbus(self):
        tries = 0
        while tries<= 10 and self.dbus_connected == False:
            try:
                self.dbus_connect(tries)
                time.sleep(0.05)
                tries += 1
            except Exception as e:
                raise e
        return self.dbus_connected

    def dbus_connect(self, attempts):
        #read dbus files generated earlier
        bus_address_filename = "/tmp/omxplayerdbus.{}".format(self.dbus_user)
        bus_pid_filename = "/tmp/omxplayerdbus.{}.pid".format(self.dbus_user)

        #first must successfully find the bus address file
        if not os.path.exists(bus_address_filename):
            self.logger.info('attempt '+str(attempts) + 'cannot find the debus addressfile') #need to include object and thread info
            return False
        #read address and check validity
        else:
            file = open(bus_address_filename, 'r')
            bus_address = file.read().rstrip()
            if bus_address == '':
                self.logger.info('attempt ' + str(attempts) + ' resulted in an empty dbus address read') #need to include object and thread info
                return False
            #check the existence of dbus pid file
            else:
                if not os.path.exists(bus_pid_filename):
                    self.logger.info('attempt ' + str(attemps) + ' cannot find dbus pid file')
                    return False
                #read the pid and check validity
                else:
                    file = open(bus_pid_filename, 'r')
                    bus_pid = file.read().rstrip()
                    if bus_pid == '':
                        self.logger.info('attempt ' + str(attempts) + ' resulted in an empty dbus pid read')
                        return False
                    else:
                        os.environ["DBUS_SESSION_BUS_ADDRESS"] = bus_address
                        os.environ["DBUS_SESSION_BUS_PID"] = bus_pid
                        self.dbus_found = True

        #
        if self.dbus_found is True:
            session_bus = dbus.SessionBus()
            try:
                omx_object = session_bus.get_object(self.dbus_name, "/org/mpris/MediaPlayer2", introspect=False)
                self.dbus_root = dbus.Interface(omx_object, "org.mpris.MediaPlayer2")
                self.dbus_props = dbus.Interface(omx_object, "org.freedesktop.DBus.Properties")
                self.dbus_player = dbus.Interface(omx_object, "org.mpris.MediaPlayer2.Player")
            except dbus.exceptions.DBusException as e:
                #log.error('attempt ' + str(attempts) + ' failed to connect to dbus: ' + e.get_dbus_message())
                return False
        self.dbus_connected = True
        return True





