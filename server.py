#-*-coding: utf-8-*-
from flask import Flask, render_template, request, session, abort, url_for, redirect
from flask_socketio import SocketIO, send
from markupsafe import escape
from stock import get_history, get_name, get_current_value
from market import afterHours

#CODES = ["GME"]


CACHED_AFTER_HOURS = {}

app = Flask(__name__)
socketio = SocketIO(app)

def auth(session):
	return False



@socketio.on('message')
def handleMessage(msg):
	try:
		if auth(session):
			command, *args = msg.split()
			return_value = {"type": command, "data": {}}
			if command == "history":
				time = int(args[1])
				data = get_history(args[0], time)
				return_value["data"] = data


			elif command == "update":
				if afterHours():
					if args[0] in CACHE:
						value = CACHE[args[0]]

					else:
						value = get_current_value(args[0])
						CACHED_AFTER_HOURS[args[0]] = value

				else:
					if len(CACHED_AFTER_HOURS):
						CACHED_AFTER_HOURS = {}
					value = get_current_value(args[0])
				return_value["data"] = value

			elif command == "name":
				name = get_name(args[0])

				return_value["data"] = name

			send(return_value)
		else:
			send({"type": "unauth"})
	except:			
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