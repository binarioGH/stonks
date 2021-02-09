#-*-coding: utf-8-*-
from flask import Flask, render_template, request, session, abort
from flask_socketio import SocketIO, send
from markupsafe import escape
from history import get_history


CODES = ["GME"]




app = Flask(__name__)
socketio = SocketIO(app)

def auth(session):
	return True



@socketio.on('message')
def handleMessage(msg):
	if auth(session):
		command, *args = msg.split()
		return_value = {"type": command, "data": {}}
		if command == "history":
			data = get_history(args[0])
			return_value["data"] = data


		elif command == "update":
			value = get_current_value()
			return_value["data"] = value

		send(return_value)
	else:
		abort(404)



@app.errorhandler(404)
def not_found(*args, **kwargs):
	return render_template("not_found.html")

@app.route("/stocks/<code>")
def stock_table(code):
	if auth(session):
		code = code.upper()
		if code in CODES:
			return render_template("stock_table.html", code=code)

	else:
		abort(404)



app.run()