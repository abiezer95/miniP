
from app import app
from flask import render_template


# @app.route("/")
# def index():
#     return render_template("home.html", data='prueba')

@app.route("/")
def chat():
    return render_template("chat.html", data='prueba')

# @socketio.on('message')
# def handleMessage(msg):
#     print('message')