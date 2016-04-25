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

class FragmentOverlap(Exception):
    pass

def read_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LISTEN_IP, LISTEN_PORT))

    while True:
        data, addr = sock.recvfrom(1024)
        data = data.strip().split(',')
        try:
            data[1] = int(data[1])
            data[2] = int(data[2])
        except ValueError as e:
            print 'bogus data! {}'.format(data)
            continue

        yield data

class FragmentBuffer(object):

    def __init__(self, fragment):
        self.fragments = []
        self.frag_count = fragment[1]
        self.fragments.append(fragment)
        self.ttl = 2

    def add(self, fragment):
        """ append a fragment to the list and check sequence ID matches if possible """

        if self.fragments[0][3] == fragment[3]:
            self.fragments.append(fragment)
        else:
            #TODO: handle this better
            log.error('Got a a fragment overlap!')
            log.debug('old: {}'.format(self.fragments[0]))
            log.debug('new: {}'.format(fragment))
            raise FragmentOverlap()

    def keep_waiting(self):
        """ decrement a per packet ttl during which we will continue to wait for more parts to
        a multipart message and give up when it's over """
        if self.ttl == 0:
            return False
        else:
            self.ttl -= 1
            return True 

    def is_complete(self):
        return self.frag_count == len(self.fragments)

    def get_fragments(self):
        """ return concatenation of data fragments and padding for decode """
        frags = ''.join(frag[5] for frag in self.fragments)
        # not sure what this is for but it seems to be necessary
        # found it here: https://github.com/schwehr/libais/blob/master/test/test_decode.py#L20
        pad = int(self.fragments[-1][6].split('*')[0][-1])
        return frags, pad

if __name__ == '__main__':

    buf = None

    for data in read_socket():
        # check on a buffer if it exists and destroy it if its waited too long
        if buf is not None:
            if not buf.keep_waiting():
                log.debug('Expiring buffer TTL')
                del buf
                buf = None

        # decode immediately if message length is one
        if data[1] == 1:
            pprint(ais.decode(data[5]))

        # buffer multi-packet messages
        else:
            log.debug('starting multipacket fragment buffer')
            if buf is None:
                buf = FragmentBuffer(data)
                continue
            else:
                try:
                    buf.add(data)
                except FragmentOverlap as e:
                    # give up if we get confused about two different multipacket messages coming in too close
                    del buf
                    buf = None
                    continue

                if buf.is_complete():
                    frags, pad = buf.get_fragments()
                    print 'MULTIPACKET!'
                    pprint(ais.decode(frags, pad))
                    del buf
                    log.debug('completed multipacket fragment buffer')
                    buf = None
