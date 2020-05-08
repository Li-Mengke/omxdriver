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
        #logging.basicConfig(filename='/home/pi/PycharmProjects/untitled/app.log', filemode = 'a', format = '%(name)s - $(levelname)s - %(message)s')
        #logging.basicConfig(level = logging.DEBUG)
        logging.debug('first log')
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

        # get options passed in
        if options is not None:
            if 'volume' in options:
                self.volume = options['volume']

    def load(self, track, cmd_options = None):

        #getting the user
        self.dbus_user = os.environ['USER']

        #generate a ordered id
        self.id = str(int(time.time()*100))
        self.dbus_name = "org.mpris.MediaPlayer2.omxplayer" + self.id


        #generate the command to call
        if cmd_options == None or cmd_options == '':
            self.omxplayer_cmd = OmxDriver.omx_command + " --dbus_name '" + self.dbus_name + "' " + track
        else:
            self.omxplayer_cmd = OmxDriver.omx_command + options + " --dbus_name '"+ self.dbus_name + "' " + track


        #start the process and get its pid
        self.process = subprocess.Popen(self.omxplayer_cmd, shell=True,stdout=open('/dev/null','a'),stderr=open('/dev/null','a'))
        self.pid = self.process.pid

        #connect to dbus
        result = self.wait_for_dbus()

        #check and update status
        self.player_running = self.process_is_running()

        #pause video at beginning
        #!!!!!!!!!!!!!!!!!!!!!!!
        return result

    def pause(self, reason = ''):
        #pause the video on signal
        self.status = self.check_status


    def exit(self, reason):
        #if process is running, try exiting. Otherwise, log error
        if self.process_is_running():
            try:
                self.dbus_root.Quit()
                return True
            except dbus.exceptions.DBusException as ex:
                logging.error('failed to exit because of a dbus error')
                return False
        else:
            logging.error('the process is not runing while trying to exit')
            return False

    def process_is_running(self, reason = ''):
        #check the status of the player when called
        if self.process.poll() == None:
            return True
        else:
            return False


    def wait_for_dbus(self):
        tries = 0
        while tries<=5 and self.dbus_connected == False:
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
            except dbus.exceptions.DBusException as ex:
                logging.info('attempt ' + str(attempts) + ' failed to connect to dbus')
                return False
        self.dbus_connected = True
        return True





