import dbus
import os
import sys
import signal
import subprocess
import time
import logging


class OmxDriver():

    omx_command = 'omxplayer --no-keys '

    def __init__(self, widget, options = None):
        #configure logging
        logging.basicConfig(filename='app.log', filemode='a',
                            format='%(name)s - %(thread)d - %(levelname)s - %(message)s', level = logging.DEBUG)
        #initiate passed-in parameters
        self.widget = widget

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
            logging.error('failed to connect to dbus after multiple attempts, killing program')
            self.terminate()

        #check and update status
        self.player_running = self.process_is_running()

        #get duration
        self.duration = self.check_duration()
        if self.duration <0:
            logging.error('failed to get duration of track, terminating program')
            self.terminate('failed to get duration of track')

        #if not the first track loaded, pause at the very beginning

        return result

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
                    logging.error('failed to pause player because of a dbus error ' + e)
                paused = self.player_is_paused()
                if paused == 'Paused':
                    self.paused = True
                    return True
                if paused == None:
                    logging.error('pause failed becasue failed to check pause status from dbus')
                    return False
            return False
        else:
            logging.warning('trying to pause when the process is not running')


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
                    logging.error('failed to check track duration: ' + e)
            else:
                logging.warning('trying to check duration when process is not running')
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
            logging.error('failed to set volume through dbus: ' + e)
            return False


    def exit(self, reason):
        #if process is running, try exiting. Otherwise, log error
        if self.process_is_running():
            try:
                self.dbus_root.Quit()
                return True
            except dbus.exceptions.DBusException as e:
                logging.error('failed to exit because of a dbus error: '+e)
                return False
        else:
            logging.error('the process is not runing while trying to exit')
            return False

    def terminate(self, reason):
        logging.critical('terminating the program, becasue: ' + reason)
        self.process.send_signal(signal.SIGINT)
        sleeptime = 0.1
        time.sleep(sleeptime)
        if self.process_is_running():
            logging.error(f'process is still running %f s after keyboard interrupt is sent', sleeptime )
            self.terminate('failed to terminate, trying again')
        else:
            logging.info('process terminated')
            exit()

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
                logging.warning('faled to check player status: ' + e)
                return None
            return result
        else:
            self.warning('process is not running, cannot test player')
            return None

    def get_position(self):
        position_ms = -1
        if self.process_is_running()
            try:
                position_ms = self.dbus_props.Position()
            except dbus.exceptions.DBusException as e:
                logging.warning('failed to get position, running on: ' + e)
        else:
            logging.warning('trying to get position when process is not running')
        return position_ms

    def mute(self):
        if self.process_is_running():
            try:
                self.dbus_player.Mute()
                return True
            except dbus.exceptions.DBusException as e:
                logging.warning('failed to mute player: ' + e)
                return False

    def unmute(self):
        if self.process_is_running():
            try:
                self.dbus_player.Unmute()
                return True
            except dbus.exceptions.DBusException as e:
                logging.warning('failed to unmute player: ' + e)
                return False

    def wait_for_dbus(self):
        tries = 0
        while tries<=2 and self.dbus_connected == False:
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
            logging.info('attempt '+str(attempts) + 'cannot find the debus addressfile') #need to include object and thread info
            return False
        #read address and check validity
        else:
            file = open(bus_address_filename, 'r')
            bus_address = file.read().rstrip()
            if bus_address == '':
                logging.info('attempt ' + str(attempts) + ' resulted in an empty dbus address read') #need to include object and thread info
                return False
            #check the existence of dbus pid file
            else:
                if not os.path.exists(bus_pid_filename):
                    logging.info('attempt ' + str(attemps) + ' cannot find dbus pid file')
                    return False
                #read the pid and check validity
                else:
                    file = open(bus_pid_filename, 'r')
                    bus_pid = file.read().rstrip()
                    if bus_pid == '':
                        logging.info('attempt ' + str(attemps) + ' resulted in an empty dbus pid read')
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
                logging.error('attempt ' + str(attempts) + ' failed to connect to dbus: ' +e)
                return False
        self.dbus_connected = True
        return True





