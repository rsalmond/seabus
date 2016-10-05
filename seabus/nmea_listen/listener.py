import socket
import os
import ais
import StringIO
import json
import logging
from logging.config import fileConfig
from memcached import mc_client

from models import Boat, Telemetry, Base, engine

LISTEN_IP = '10.8.0.1'
LISTEN_PORT  = 3000
#LISTEN_IP = '0.0.0.0'
#LISTEN_PORT  = 3001

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log.addHandler(sh)

def read_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LISTEN_IP, LISTEN_PORT))

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

def read_payload(fragment):
    data = fragment.strip().split(',')
    try:
        data[1] = int(data[1])
        data[2] = int(data[2])
    except ValueError as e:
        print 'bogus data! {}'.format(data)

    return data

def is_interesting(beacon):
    # http://catb.org/gpsd/AIVDM.html#_ais_payload_interpretation
    return beacon.get('id') > 5

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    for data in read_socket():
        beacon = decode(data)
        if beacon is not None:
            if is_interesting(beacon):
                log.info('Interesting beacon type: {}'.format(beacon.get('id')))
                log.info(beacon)
    
            boat = Boat.from_beacon(beacon)
            telemetry = Telemetry.from_beacon(beacon)

            if None not in (boat, telemetry):
                if boat.is_seabus:
                    # write telemetry to memcached for seabus
                    cached_telemetry = {'lat': telemetry.lat, 'lon': telemetry.lon}
                    mc_client.set(str(boat.mmsi), cached_telemetry)

                # write to db for every boat
                telemetry.record_for_boat(boat)

                log.info(telemetry)
