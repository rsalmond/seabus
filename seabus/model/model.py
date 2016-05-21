#from .common.bounding_boxes import WATERFRONT, LONSDALE
from ..common import bounding_boxes
import pandas as pd
import sqlite3

def loadbus(bus=None):
    con = sqlite3.connect('test.db')
    return pd.read_sql_query('select * from telemetry where boat_id =5', con, parse_dates=['received'], index_col=['received']) 

def label_dockings(data):
    """ add a label to indicate when the bus was stopped at one of the docks """
    pass

def label_arrive(data):
    """ add a label to indicate when the bus arrives at one of the docks """
    pass

def label_depart(data):
    """ add a label to indicate when the bus departs one of the docks """

if __name__ == '__main__':
    data = loadbus()
