from flask import Flask, render_template
# from flask_socketio import SocketIO, send

# from werkzeug.debug import DebuggedApplication
app = Flask(__name__, template_folder="config/views", static_folder="config/assets")

app.config.from_pyfile('config.py') #calling all the configurations of flask

jinja_options = app.jinja_options.copy()
jinja_options.update(dict(
    variable_start_string = '(%',
    variable_end_string= '%)'
))

app.jinja_options = jinja_options #changing the special characters to call jinja variables

# socketio = SocketIO(app) 

# @socketio.on('message')
# def handleMessage(msg):
#     print(msg)
#     send(msg, broadcast = True)

from routes import *

if __name__ == "_main_":
    app.run()
    # socketio.run(app)
    