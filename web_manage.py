#!/usr/bin/env python

import flask_migrate
import flask_script

from seabus.web.socketio import socketio
from seabus.common.database import db
from seabus.web.web import create_app as create_web_app
from seabus.nmea_listen.listener import listen

web_app = create_web_app('Dev')

web_manager = flask_script.Manager(web_app)

flask_migrate.Migrate(web_app, db)
web_manager.add_command('db', flask_migrate.MigrateCommand)

@web_manager.command
def webdev():
    socketio.run(
        web_app,
        host='0.0.0.0',
        debug=True,
        use_reloader=True,
    )

@web_manager.command
def webprod():
    web_app.config.from_object('seabus.web.config.Prod')
    socketio.run(
        web_app,
        debug=False,
        use_reloader=False,
    )

@web_manager.command
def listendev():
    listen(web_app.config)

@web_manager.command
def listenprod():
    web_app.config.from_object('seabus.web.config.Prod')
    listen(web_app.config)

@web_manager.command
def debug():
    from seabus.common.models import Telemetry, Boat
    from seabus.common.telemetry import seabus_telemetry
    import pdb
    pdb.set_trace()

if __name__ == '__main__':
    web_manager.run()
