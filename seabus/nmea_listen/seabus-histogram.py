from models import Boat, Telemetry
from pandas import DataFrame
from haversine import haversine
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def go(bus=None):
    tuner_position = (49.284768, -123.109248)
    seabuses = Boat.all_seabuses()
    print seabuses[bus].name
    telemetry = [rec.__dict__ for rec in seabuses[bus].telemetry]
    df = DataFrame.from_records(telemetry)
    df['dist'] = [haversine(pos, tuner_position) for pos in zip(df.lat, df.lon)]
    return df, seabuses

if __name__ == '__main__':
    BUS = 1
    bunk, buses = go(BUS)
    #bunk['dist'].hist()
    #bunk[(bunk['nav_status'] == 0)]['dist'].hist()
    #bunk[(bunk['received'] > '2016-05-04 06:00') & (bunk['received'] < '2016-05-05')]['dist'].hist()
    bunk['timestamp'].hist(bins=6)
    plt.suptitle('{} position data'.format(buses[BUS].name))
    plt.ylabel('beacons received')
    plt.xlabel('seconds after the minute')
    #plt.yticks(range(60), [0, 10, 20, 30, 40, 50, 60])
    plt.show()
