#!/bin/bash

LISTEN_SCRIPT=~/listener.sh

date
echo "INFO: Finalizing calibration process."

START_PID=$(ps -ef | grep rtl_test | grep -v grep | awk '{print $2}')

# if we find a pid, stop the calibration logging process
if [ ! -z $START_PID ]; then
	echo "INFO: Stopping process: $START_PID ..."
	kill -INT $START_PID
else
	# if process didnt run for some reason, try to use the old ppm_calibrate.log file
	echo "ERR: Calibration process not running, attempting to use stale data."
fi

echo "INFO: Resetting rtl-sdr"

# http://askubuntu.com/questions/645/how-do-you-reset-a-usb-device-from-the-command-line
sudo sh -c "echo 0 > /sys/bus/usb/devices/1-1.2/authorized"
sudo sh -c "echo 1 > /sys/bus/usb/devices/1-1.2/authorized"

PPM=$(grep "cumulative" /tmp/ppm_calibrate.log | tail -n 1 | awk '{print $10}')


# don't update script if we have no PPM value
if [ ! -z $PPM ]; then
	echo "INFO: updating listener with PPM: $PPM"
	echo "#!/bin/bash" > $LISTEN_SCRIPT
	echo "/home/pi/rtl-ais/rtl_ais -p $PPM -n -h 10.8.0.1" >> $LISTEN_SCRIPT
	chmod +x $LISTEN_SCRIPT
else
	echo "ERR: no PPM value found, calibration fail!"
fi

echo "INFO: starting listener"

sudo supervisorctl start rtlais
