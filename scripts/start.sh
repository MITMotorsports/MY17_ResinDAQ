#!/bin/bash

# Enable PiCAN2
sudo /sbin/ip link set can0 up type can bitrate 500000
