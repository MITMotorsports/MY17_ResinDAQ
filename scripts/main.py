'''
MIT LICENSE

Copyright 2014 Inertial Sense, LLC - http://inertialsense.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions :

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import sys

from time import sleep
from pySDK.inertialsensemodule import InertialSense, pyUpdateFlashConfig
from pySDK.display import cInertialSenseDisplay
from pySDK.logger import cISLogger
import pySDK.isutilities as util

# TODO: Make Defaults, Definitions and Member Variables available directly from C++ or put them in another python module
IS_COM_BAUDRATE_DEFAULT = 3000000
DEFAULT_LOGS_DIRECTORY = "IS_logs"
DMODE_PRETTY = 0
DMODE_SCROLL = 1
DMODE_STATS = 2
DMODE_QUITE = 3

def main():
    display = cInertialSenseDisplay()
    cltool_main()

def cltool_dataCallback(data):

    #print "Callback 2 - Received msg: %d" % data['header']['id']

    # Example for data access
    DID_INS_2 = 5
    DID_DUAL_IMU = 58
    DID_DELTA_THETA_VEL = 3
    DID_GPS = 5
    DID_MAGNETOMETER_1 = 52
    DID_MAGNETOMETER_2 = 55
    DID_BAROMETER = 53
    DID_RAW_DATA = 60

    if data['header']['id'] == DID_INS_2:
        #print "qn2b Data Legth %d" % len(data['data']['qn2b'])     # quaternion attitude
        #print "Quaternions: %f, %f, %f, %f" % (data['data']['qn2b'][0],data['data']['qn2b'][1],data['data']['qn2b'][2],data['data']['qn2b'][3])
        data['data']['qn2b']     # quaternion attitude
        data['data']['uvw']      # body velocities
        data['data']['lla']      # latitude, longitude, altitude

    elif data['header']['id'] == DID_DUAL_IMU:
        data['data']['time'];
        data['data']['imu1acc']
        data['data']['imu1pqr']
        data['data']['imu2acc']
        data['data']['imu2pqr']

    elif data['header']['id'] == DID_DELTA_THETA_VEL:
        data['data']['time']
        data['data']['theta']
        data['data']['uvw']
        data['data']['dt']

    elif data['header']['id'] == DID_GPS:
        data['data']['tOffset']
        data['data']['gpsPos']
        data['data']['gpsVel']
        data['data']['rxps']

    elif data['header']['id'] == DID_MAGNETOMETER_1:
        data['data']['time']
        data['data']['mag']

    #elif data['header']['id'] == DID_MAGNETOMETER_2:       # See Mag 1
    elif data['header']['id'] == DID_BAROMETER:
        data['data']['time']
        data['data']['bar']
        data['data']['barTemp']
        data['data']['humidity']
        data['data']['mslBar']

    elif data['header']['id'] == DID_RAW_DATA:
        print("Received the Raw message in Python!")
        data['data']['receiverIndex']
        data['data']['type']  # Indicates the message type
        data['data']['count']
        data['data']['reserved']
        data['data']['buf']   # 1020 byte buffer
        # Handle the different GPS Raw messages here

    # elif ... (add other messages here)

def cltool_main(comPort):
    baudRate=IS_COM_BAUDRATE_DEFAULT
    #clear display
    display.SetDisplayMode(False);
    display.Clear();

    # open the device, start streaming data and logging

    # [COMM INSTRUCTION] 1.) Create InertialSense object and open serial port. if reading/writing flash config, don't bother with data callback
    inertialSenseInterface = InertialSense()
    inertialSenseInterface.SetPyCallback(self.cltool_dataCallback)
    inertialSenseInterface.SetPyDisplay(display)
    if not inertialSenseInterface.Open(comPort, baudRate):
        raise RuntimeWarning("Failed to open serial port at {} - {}".format(comPort, baudRate)

    # [COMM INSTRUCTION] 2.) Enable data broadcasting from uINS
    if __cltool_setupCommunications():
        # [LOGGER INSTRUCTION] Setup and start data logger
        __cltool_setupLogger();

    try:
        # Main loop. Could be in separate thread if desired.
        while True:
            # [COMM INSTRUCTION] 3.) Process data and messages
            inertialSenseInterface.Update();
            if inertialSenseInterface.GetTcpByteCount() != 0:
                display.GoToRow(1);
                print("Tcp bytes read: {}".format(inertialSenseInterface.GetTcpByteCount()))

            # Specify the minimum time between read/write updates.
            sleep(.001);

    except Exception as e:
        print("Unknown exception, {}".format(str(e)))

    except:
        # Catch System Exit or Keyboard Interupt
        pass

    print "Shutting down..."

    # close the interface cleanly, this ensures serial port and any logging are shutdown properly
    inertialSenseInterface.Close();
    return 0;

def __cltool_setupCommunications():
    periodMs = 50;
    inertialSenseInterface.StopBroadcasts();    # Stop streaming any prior messages

    # ask for device info every 2 seconds
    DID_DEV_INFO = 1
    inertialSenseInterface.PyBroadcastBinaryData(DID_DEV_INFO, 2000);

    # depending on command line options. stream various data sets
    inertialSenseInterface.SetBroadcastSolutionEnabled(true);

    DID_INS_1 = 4
    inertialSenseInterface.PyBroadcastBinaryData(DID_INS_1, periodMs);

    DID_INS_2 = 5
    inertialSenseInterface.PyBroadcastBinaryData(DID_INS_2, periodMs);

    DID_SYS_SENSORS = 11
    inertialSenseInterface.PyBroadcastBinaryData(DID_SYS_SENSORS, 100);

    DID_DUAL_IMU = 58
    inertialSenseInterface.PyBroadcastBinaryData(DID_DUAL_IMU, periodMs);

    DID_IMU_1 = 2
    inertialSenseInterface.PyBroadcastBinaryData(DID_IMU_1, periodMs);

    DID_IMU_2 = 54
    inertialSenseInterface.PyBroadcastBinaryData(DID_IMU_2, periodMs);

    DID_DELTA_THETA_VEL = 3
    inertialSenseInterface.PyBroadcastBinaryData(DID_DELTA_THETA_VEL, periodMs);

    DID_GPS = 6
    inertialSenseInterface.PyBroadcastBinaryData(DID_GPS, 200);

    DID_MAGNETOMETER_1 = 52
    inertialSenseInterface.PyBroadcastBinaryData(DID_MAGNETOMETER_1, periodMs);

    DID_BAROMETER = 53
    inertialSenseInterface.PyBroadcastBinaryData(DID_BAROMETER, periodMs);

    DID_RAW_DATA = 60
    inertialSenseInterface.PyBroadcastBinaryData(DID_RAW_DATA, periodMs);

    return True

def __cltool_setupLogger():
    # Enable logging in continuous background mode
    inertialSenseInterface.SetLoggerEnabled(
        self.opts.enableLogging, # enable logger
        self.opts.logPath, # path to log to, if empty defaults to DEFAULT_LOGS_DIRECTORY
        self.opts.logSolution, # solution logging options
        self.opts.maxLogSpaceMB, # max space in mb to use, 0 for unlimited - only MAX_PERCENT_OF_FREE_SPACE_TO_USE_FOR_IS_LOGS% of free space will ever be allocated
        self.opts.maxLogFileSize, # each log file will be no larger than this in bytes
        self.opts.maxLogMemory, # logger will try and keep under this amount of memory
        self.opts.useLogTimestampSubFolder # whether to place log files in a new sub-folder with the current timestamp as the folder name
    )

if __name__ == "__main__":
    main()
