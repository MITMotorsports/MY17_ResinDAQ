#!/bin/bash

# Determine comports
INSC='/dev/ttyUSB0'

# Establish file structure
mkdir -p /data/CAN_logs
mkdir -p /data/INS_logs

# Start button manager
btnmgr &
echo 'Button manager up!'

# Configure status PIN_led
gpio mode ${PIN_led} OUTPUT
gpio write ${PIN_led} 1

sleep 2

# Enable and start CAN Logging
# sudo /sbin/ip link set can0 up type can bitrate 500000
# cd ${DIRE}/CAN_logs
# candump -l any,0:0,#FFFFFFFF 2>> ${DIRE}/logoflogs &

# Start INS Logging
cltool -sINS1 -sINS2 -sDualIMU -sIMU1 -sIMU2 -sGPS -sMag1 -sBaro -sSensors -sDThetaVel -c="${INSC}" -lp="/data/INS_logs" > /dev/null 2>&1 &
echo 'INS logging up!'

# Blink
echo 'Setup DONE!'
gpio blink ${PIN_led}
