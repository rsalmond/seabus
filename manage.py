#!/usr/bin/env python

import flask_migrate
import flask_script

from seabus.web.socketio import socketio
from seabus.common.database import db
from seabus.web.web import create_app
from seabus.nmea_listen.listener import listen

app = create_app('Dev')
manager = flask_script.Manager(app)
flask_migrate.Migrate(app, db)
manager.add_command('db', flask_migrate.MigrateCommand)

@manager.command
def rundev(debug=True, use_reloader=True):
    socketio.run(
        app,
        host='0.0.0.0',
        debug=debug,
        use_reloader=use_reloader,
    )

@manager.command
def listener():
    listen(app.config)

if __name__ == '__main__':
    manager.run()
