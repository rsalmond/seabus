#!/usr/bin/env python

import flask_migrate
import flask_script

from seabus.web.socketio import socketio
from seabus.common.database import db
from seabus.web.web import create_app
from seabus.nmea_listen.listener import listen

tv_app = create_app('Dev')
app = tv_app.wrapped_app
manager = flask_script.Manager(app)
flask_migrate.Migrate(app, db)
manager.add_command('db', flask_migrate.MigrateCommand)

@manager.command
def webdev():
    socketio.run(
        app,
        host='0.0.0.0',
        debug=True,
        use_reloader=True,
    )

@manager.command
def webprod():
    app.config.from_object('seabus.web.config.Prod')
    socketio.run(
        app,
        debug=False,
        use_reloader=False,
    )

@manager.command
def listendev():
    listen(app.config)

@manager.command
def listenprod():
    app.config.from_object('seabus.web.config.Prod')
    listen(app.config)

if __name__ == '__main__':
    manager.run()
