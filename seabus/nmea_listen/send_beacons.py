#!/usr/bin/env python
import pdb
import socket
from time import sleep

def send_packet(data):
    host = '127.0.0.1'
    port = 3001
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data, (host, port))


def iterbeacons():
    with open('seabus_beacons.txt', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line.count('!AIVD') > 1:
                left, middle, right = line.rpartition('!AIVD')
                right = ''.join((middle, right))
                yield '{}\r\n{}'.format(left, right)
            else:
                yield line

def sendbeacons():
    for line in iterbeacons():
        send_packet(line)
        sleep(1)

if __name__ == '__main__':
    sendbeacons()
