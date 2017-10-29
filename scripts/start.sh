#!/bin/bash

# Determine comports
INSC = '/dev/ttyUSB0'

# Establish file structure
mkdir -p /data/CAN_logs
mkdir -p /data/INS_logs

# Enable PiCAN2
/sbin/ip link set can0 up type can bitrate 500000
cd /data/CAN_logs
#/usr/src/app/candump -l any,0:0,#FFFFFFFF 2>> /data/CAN_logs/logoflogs &

# Start INS Logging
#cltool -c="${INSC}" -lp="${LOGDIR}INS_logs" -sINS1 -sINS2 -sDualIMU -sIMU1 -sIMU2 -sGPS -sMag1 -sBaro -sSensors -sDThetaVel &
