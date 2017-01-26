#!/bin/bash

FILE=/tmp/ppm_calibrate.log

date
echo "INFO: Starting calibration process."

sudo supervisorctl stop rtlais

echo "INFO: Resetting rtl-sdr"

# http://askubuntu.com/questions/645/how-do-you-reset-a-usb-device-from-the-command-line
sudo sh -c "echo 0 > /sys/bus/usb/devices/1-1.2/authorized"
sudo sh -c "echo 1 > /sys/bus/usb/devices/1-1.2/authorized"

# clear out last run
rm -rf $FILE

echo "INFO: Executing calibration."

stdbuf -oL rtl_test -p 30 &> $FILE
