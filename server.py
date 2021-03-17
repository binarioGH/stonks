#-*-coding: utf-8-*-
from flask import Flask, render_template, request, session, abort, url_for, redirect
from flask_socketio import SocketIO, send
from markupsafe import escape
from stock import *
from market import afterHours
from json import loads
from mysql.connector import connect
from hashlib import sha256
from random import randint, choice
from validate_email import validate_email
#CODES = ["GME"]



#stonks ~ select
#KwoqBdeRrwnDgZ4o

ACTIVE_COOKIES = {}
SYMBOLS = {}

TOOLS = {"sql": connect(host='127.0.0.1', user='stonks', password='KwoqBdeRrwnDgZ4o', database='stonks')}
cursor = TOOLS["sql"].cursor()
cursor.execute("SELECT username, password FROM users;")
response = cursor.fetchall()
print(response)

with open("symbols.json", "r") as f:
	SYMBOLS = loads(f.read())


app = Flask(__name__)
app.secret_key = '''blocked_chars = ("<", ">", ";", "'", "SELECT", "UPDATE", "SET", "WHERE", '=')'''
socketio = SocketIO(app)



def sanitize(text):
	blocked_chars = ("<", ">", ";", "'", "SELECT", "UPDATE", "SET", "WHERE", '=')
	for blocked in blocked_chars:
		if blocked.lower() in text or blocked.upper() in text:
			return 0

	return 1 


def generate_cookie(user, password, ip):
	ABC = "abcdefghijklmnopqrstuvwxyz1234567890"
	cookie = ''
	for i in range(0, randint(10, 21)):
		letter = choice(ABC) 
		if randint(0, 1):
			letter = letter.upper()
		cookie += letter
	ACTIVE_COOKIES[cookie] = {"user": user, "password": password, "ip": ip}
	return cookie




def auth(session):
	if (not "token" in session) or (not "user" in session) or (not "password" in session):
		return False
	token = session["token"]
	
	if not token in ACTIVE_COOKIES:
		return False
	if ACTIVE_COOKIES[token]["user"] != session["user"]:
		return False

	if ACTIVE_COOKIES[token]["password"] != session["password"]:
		return False

	if session["ip"] != ACTIVE_COOKIES[token]["ip"]:
		return False

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

			elif command == "symbols":
				return_value["data"] = SYMBOLS

			send(return_value)
		else:
			send({"type": "unauth"})
	else:			
		send({"type": "error"})


@app.errorhandler(404)
def not_found(*args, **kwargs):
	return render_template("not_found.html")


@app.route("/account")
def account():
	print("ralf")
	if auth(session):
		return render_template("account.html")
	else:
		return redirect(url_for("landing"))


@app.route("/logout")
def logout():
	if auth(session):
		del ACTIVE_COOKIES[session["token"]]
		del session["user"]
		del session["password"]
		del session["ip"]
		return render_template("login.html")

	else:
		return render_template("landing.html")


@app.route("/stocks/<code>")
def stock_table(code):
	if auth(session):
		code = code.upper()
		
		return render_template("stock_table.html", code=code)

	else:
		abort(404)

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == 'POST':
		if "user" in request.form and "password" in request.form:
			user = request.form["user"]
			password = sha256(request.form["password"].encode()).hexdigest()
			cursor = TOOLS["sql"].cursor()
			query = "SELECT username, password FROM users WHERE username=%s;"
			cursor.execute(query, (user,))
			results = cursor.fetchall()
			if len(results):
				q_user, q_password = results[0]
				if user == q_user and password == q_password:
					token = generate_cookie(user, password, request.remote_addr)
					session["token"] = token
					session["user"] = user
					session["password"] = password
					session["ip"] = request.remote_addr
					print(session)
					print(ACTIVE_COOKIES)
					return redirect(url_for("landing"))
		

	if not auth(session):
		return render_template("login.html")

	return redirect(url_for("landing"))


@app.route("/")
def landing():
	if auth(session):
		return render_template("logged.html")

	else:
		return render_template("landing.html")



app.run()