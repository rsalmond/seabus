#Seab.us
=======

Here's the code for the app which drives [seab.us](http://seab.us).

#Listener
The [listener](seabus/nmea_listen/listener.py) program receives and processses marine telemetry data relayed from a raspberry pi with an [RTL-SDR](http://www.rtl-sdr.com/about-rtl-sdr/) tuner running [aisdecoder](https://github.com/sailoog/aisdecoder) to decode [AIS beacons](https://en.wikipedia.org/wiki/Automatic_identification_system).

#Web
The [flask app](seabus/web/) provides near realtime access to the seabus telemetry data via websocket push updates.

#Hacking
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

#API

There is an experimental API read endpoint available at [http://api.seab.us/data/v1](http://api.seab.us/data/v1). At the moment it requires no access key and provides the same data delivered to the web front end. Both of these things may change, watch this space!
