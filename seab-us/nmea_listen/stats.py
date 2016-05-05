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
    telemetry = [rec.__dict__ for rec in seabuses[bus].telemetry]
    df = DataFrame.from_records(telemetry)
    df['dist'] = [haversine(pos, tuner_position) for pos in zip(df.lat, df.lon)]
    return df

if __name__ == '__main__':  
    bunk = go(1)
    #bunk['dist'].hist()
    #bunk[(bunk['nav_status'] == 0)]['dist'].hist()
    bunk[(bunk['received'] > '2016-05-04 06:00') & (bunk['received'] < '2016-05-05')]['dist'].hist()
    plt.show()
