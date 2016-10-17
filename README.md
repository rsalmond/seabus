#seabus
=======

Here's most of the code for the app which drives [seab.us](http://seab.us).

#listener
The [listener](seabus/nmea_listen/listener.py) program receives and processses marine telemetry data relayed from a raspberry pi with an [RTL-SDR](http://www.rtl-sdr.com/about-rtl-sdr/) tuner running [aisdecoder](https://github.com/sailoog/aisdecoder) to decode [AIS beacons](https://en.wikipedia.org/wiki/Automatic_identification_system).

#web
The [flask app](seabus/web/) provides near realtime access to the seabus telemetry data via websocket push updates.

#hacking
The vagrantfile will get you most of the way to a working dev environment, may be a bit wonky though.

To set up:

* Activate virtualenv.
```
vagrant@vagrant-ubuntu-trusty-64:~/seabus$ source seabus/.venv/bin/activate
```

* Initialize empty database.
```
(.venv) vagrant@vagrant-ubuntu-trusty-64:~/seabus$ ./manage.py db upgrade
```

To run the web app:
```
(.venv) vagrant@vagrant-ubuntu-trusty-64:~/seabus$ ./manage.py rundev
```

To run the listener:
```
(.venv) vagrant@vagrant-ubuntu-trusty-64:~/seabus$ ./manage.py listendev
```

To send a few recorded seabus AIS update beacons to the running listener:
```
(.venv) vagrant@vagrant-ubuntu-trusty-64:~/seabus/seabus/nmea_listen$ ./sendbeacons.sh seabus_beacons.txt 
```
