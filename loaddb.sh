#!/bin/bash

sqlite3 db_seabus.db 'attach "../orig.db" as orig; insert into boats select * from orig.boats; insert into telemetry select * from orig.telemetry;'
