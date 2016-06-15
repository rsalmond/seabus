#from .common.bounding_boxes import WATERFRONT, LONSDALE
import pandas as pd
import geopandas as gpd
from geopandas import GeoSeries, GeoDataFrame
from geopandas.tools import sjoin
import sqlite3
from shapely.geometry import Point
from ..common.bounding_boxes import bounds

def loadbus(bus=None):
    con = sqlite3.connect('test.db')
    df = pd.read_sql_query('select * from telemetry where boat_id =5', con, parse_dates=['received'], index_col=['received'])
    # geopandas requires this to be called 'geometry' 
    df['geometry'] = df.apply(lambda y: Point(y.lon, y.lat), axis=1)
    return df

def label_dockings(data):
    """ add a label to indicate when the bus was stopped at one of the docks """
    for row in data:
        import pdb
        pdb.set_trace()
    return data

def label_arrive(data):
    """ add a label to indicate when the bus arrives at one of the docks """
    pass

def label_depart(data):
    """ add a label to indicate when the bus departs one of the docks """

if __name__ == '__main__':
    print 'creating bounds'
    spots = GeoDataFrame({'geometry': [bounds['WATERFRONT'], bounds['LONSDALE'], bounds['PARKING']]})
    print 'loading bus data'
    data = loadbus()
    gdf = gpd.GeoDataFrame(data)
    print 'joining'
    #joined = sjoin(gdf, spots, how='inner', op='contains')
    import pdb
    pdb.set_trace()
