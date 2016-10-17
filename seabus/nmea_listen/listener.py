from __future__ import absolute_import

import socket
import os
import ais
import StringIO
import json
import logging
import requests
from logging.config import fileConfig

from seabus.common.memcached import mc_client
from seabus.common.models import Boat, Telemetry

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log.addHandler(sh)

def read_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))

    while True:
        message, addr = sock.recvfrom(1024)
        yield message.strip()

def decode(message):

    decoded = None

    # immediately attempt to extract payload from single part messages
    if '\r\n' not in message:
        try:
            payload = message.split(',')[5]
        except Exception as e:
            log.error('{} trying to parse message {}'.format(e, message))
            return

        try:
            decoded = ais.decode(payload, 0)
        except Exception as e:
            log.error('{} trying to decode message {}'.format(e, message))
            return

    # unpack and assemble payload from multipart messages
    else:
        fragments = message.split('\r\n')
        try:
            payload = ''.join(fragment.split(',')[5] for fragment in fragments)
        except Exception as e:
            log.error('{} trying to parse multipart message {}'.format(e, message))
            return
        # not sure what this is for but it seems to be necessary
        # found it here: https://github.com/schwehr/libais/blob/master/test/test_decode.py#L20
        pad = int(fragments[-1].split('*')[0][-1])
        try:
            decoded = ais.decode(payload, pad)
        except Exception as e:
            log.error('{} trying to decode multipart message {}'.format(e, message))
            log.debug('Payload: {}'.format(payload))
            log.debug('Pad: {}'.format(pad))
            return

    return decoded

def is_interesting(beacon):
    # http://catb.org/gpsd/AIVDM.html#_ais_payload_interpretation
    return beacon.get('id') > 5


def listen(config):
    """ 
    listen for and process incoming UDP AIS location beacons sent from the AIS Decoder process on the tuner
    """
    host = config.get('LISTENER_HOST')
    port = config.get('LISTENER_PORT')
    update_url = config.get('LISTENER_UPDATE_URL')

    log.info('Listenening for AIS beacons on {}:{}'.format(host, port))

    for data in read_socket(host, port):
        beacon = decode(data)
        if beacon is not None:
            if is_interesting(beacon):
                log.info('Interesting beacon type: {}'.format(beacon.get('id')))
                log.info(beacon)
    
            boat = Boat.from_beacon(beacon)
            telemetry = Telemetry.from_beacon(beacon)

            if None not in (boat, telemetry):
                if boat.is_seabus:
                    log.info('Seabus: {}'.format(telemetry))
                    # write telemetry to memcached for seabus
                    cached_telemetry = {'lat': telemetry.lat, 'lon': telemetry.lon}
                    mc_client.set(str(boat.mmsi), cached_telemetry)
                    # notify web app that new data is available for push to clients
                    requests.get(update_url)
                else:
                    log.info(telemetry)

                # write to db for every boat
                telemetry.record_for_boat(boat)
