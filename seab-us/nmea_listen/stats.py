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
    telemetry = []
    boats = Boat.all()
    for boat in boats:
        telemetry = [rec.__dict__ for rec in boat.telemetry]
        tmp_df = DataFrame.from_records(telemetry)
        tmp_df.index = tmp_df['received']
        tmp_df['dist'] = [haversine(pos, tuner_position) for pos in zip(tmp_df.lat, tmp_df.lon)]
        #import pdb
        #pdb.set_trace()
        return tmp_df

if __name__ == '__main__':
    bunk = go()
    #bunk['dist'].hist()
    #bunk[(bunk['nav_status'] == 0)]['dist'].hist()
    #bunk[(bunk['received'] > '2016-05-04 06:00') & (bunk['received'] < '2016-05-05')]['dist'].hist()
    #bunk['timestamp'].hist(bins=6)
    #plt.suptitle('{} position data'.format(buses[BUS].name))
    #plt.ylabel('beacons received')
    #plt.xlabel('seconds after the minute')
    #plt.yticks(range(60), [0, 10, 20, 30, 40, 50, 60])
    #plt.plot(bunk['received'].resample('10T').median(), bunk['dist'].resample('10T').count(), 'ro')
    #plt.xlabel('average distance km')
    #plt.ylabel('beacon count')
    #bunk.plot()
    thing = bunk['dist'].resample('10T', how = ['mean', 'count'])
    #thing = bunk['dist'].resample('10T').apply(np.mean, len)
    thing.plot(subplots=True)
    #plt.plot(bunk['received'].resample('10T'), bunk['dist'].resample('10T').median())
    plt.show()
