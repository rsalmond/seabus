from models import Boat, Telemetry
from pandas import DataFrame
from haversine import haversine

def loadboats():
    telemetry = []
    boats = Boat.all()
    for boat in boats:
        telemetry += [rec.__dict__ for rec in boat.telemetry]

    tmp_df = DataFrame.from_records(telemetry)
    tmp_df.index = tmp_df['received']
    tmp_df['dist'] = [haversine(pos, tuner_position) for pos in zip(tmp_df.lat, tmp_df.lon)]
    return tmp_df

if __name__ == '__main__':
    print len(loadboats())
