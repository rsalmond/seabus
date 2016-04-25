import socket
import os
import ais
import StringIO
import logging
from logging.config import fileConfig
from pprint import pprint

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

    # immediately attempt to extract payload from single part messages
    if '\r\n' not in message:
        try:
            payload = message.split(',')[5]
        except Exception as e:
            log.error('{} 1 trying to decode {}'.format(e, message))
            return

        return ais.decode(payload)

    # unpack and assemble payload from multipart messages
    else:
        fragments = message.split('\r\n')
        try:
            payload = ''.join(fragment.split(',')[5] for fragment in fragments)
        except Exception as e:
            log.error('{} 2 trying to decode {}'.format(e, message))
            return
        # not sure what this is for but it seems to be necessary
        # found it here: https://github.com/schwehr/libais/blob/master/test/test_decode.py#L20
        pad = int(fragments[-1].split('*')[0][-1])
        return ais.decode(payload, pad)
        

def read_payload(fragment):
    data = fragment.strip().split(',')
    try:
        data[1] = int(data[1])
        data[2] = int(data[2])
    except ValueError as e:
        print 'bogus data! {}'.format(data)

    return data

if __name__ == '__main__':

    buf = None

    for data in read_socket():
        print '*' * 50
        pprint(decode(data))
