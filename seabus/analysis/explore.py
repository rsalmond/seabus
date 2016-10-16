import pandas as pd
import sqlite3

con = sqlite3.connect('test.db')
df = pd.read_sql_query('select * from telemetry where boat_id =33', con)

if __name__ == '__main__':
    import pdb
    pdb.set_trace()
