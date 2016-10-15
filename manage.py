import flask_migrate
import flask_script


from seabus.web.web import app
from seabus.web.socketio import socketio

manager = flask_script.Manager(app)

@manager.command
def rundev(debug=True, use_reloader=True):
    socketio.run(
        app,
        host='0.0.0.0',
        debug=debug,
        use_reloader=use_reloader,
    )

if __name__ == '__main__':
    manager.run()
