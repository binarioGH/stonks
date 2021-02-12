#-*-coding: utf-8-*-
from flask import Flask, render_template, request, session, abort, url_for, redirect
from flask_socketio import SocketIO, send
from markupsafe import escape
from stock import *
from market import afterHours

#CODES = ["GME"]




app = Flask(__name__)
socketio = SocketIO(app)

def auth(session):
	return True





@socketio.on('message')
def handleMessage(msg):
	if True:
		if auth(session):
			command, *args = msg.split()
			return_value = {"type": command, "data": {}}
			if command == "history":
				time = int(args[1])
				data = get_history(args[0], time)
				return_value["data"] = data

			elif command == "update":
				value = get_current_value(args[0])
				return_value["data"] = value

			elif command == "name":
				name = get_name(args[0])

				return_value["data"] = name

			elif command == "hotstocks":
				stocks = get_hot_stocks()
				return_value["data"] = stocks;

			send(return_value)
		else:
			send({"type": "unauth"})
	else:			
		send({"type": "error"})


@app.errorhandler(404)
def not_found(*args, **kwargs):
	return render_template("not_found.html")


@app.route("/")
def home():
	if auth(session):
		return render_template("index.html")
	else:
		return redirect("login")

@app.route("/stocks/<code>")
def stock_table(code):
	if auth(session):
		code = code.upper()
		
		return render_template("stock_table.html", code=code)

	else:
		abort(404)

@app.route("/login")
def login():
	if not auth(session):
		return render_template("login.html")

	else:
		return redirect(url_for("home"))



app.run()