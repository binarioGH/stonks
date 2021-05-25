#-*-coding: utf-8-*-

#Import libraries
from flask import Flask, render_template, request, session, abort, url_for, redirect
from flask_socketio import SocketIO, send
from markupsafe import escape
from stock import *
from market import afterHours
from json import loads
from mysql.connector import connect
from hashlib import sha256
from random import randint, choice
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


#stonks ~ select
#KwoqBdeRrwnDgZ4o

ACTIVE_COOKIES = {} #Create list of active users
SYMBOLS = {} #Cached symbols for not having to get the data everytime

#Login into the sql database
TOOLS = {"sql": connect(host='127.0.0.1', user='root', password='', database='stonks')}
cursor = TOOLS["sql"].cursor()

#cursor.execute("SELECT username, password FROM users;")
#response = cursor.fetchall()
#print(response)

with open("symbols.json", "r") as f:
	SYMBOLS = loads(f.read()) #Get list of symbols


app = Flask(__name__)
app.secret_key = '''blocked_chars = ("<", ">", ";", "'", "SELECT", "UPDATE", "SET", "WHERE", '=')'''
socketio = SocketIO(app) #Create webscoket



def sanitize(text): #Function to sanitize data to avoid sql injection and xss
	blocked_chars = ("<", ">", ";", "'", "SELECT", "UPDATE", "SET", "WHERE", '=')
	for blocked in blocked_chars:
		if blocked.lower() in text or blocked.upper() in text:
			return 0

	return 1 


def generate_cookie(user, ip): #Create unique identifier for each user
	ABC = "abcdefghijklmnopqrstuvwxyz1234567890"
	cookie = ''
	for i in range(0, randint(10, 21)):
		letter = choice(ABC) 
		if randint(0, 1):
			letter = letter.upper()
		cookie += letter
	ACTIVE_COOKIES[cookie] = {"user": user, "ip": ip}
	return cookie




def auth(session): #Check for any extrange behavior and correct login.
	if (not "token" in session) or (not "user" in session) or (not "password" in session):
		return False
	token = session["token"]
	
	if not token in ACTIVE_COOKIES:
		return False
	if ACTIVE_COOKIES[token]["user"] != session["user"]:
		return False

	#if ACTIVE_COOKIES[token]["password"] != session["password"]:
	#	return False

	if session["ip"] != ACTIVE_COOKIES[token]["ip"]:
		return False

	return True




@socketio.on('message')
def handleMessage(msg): #Handle web sockets
	if True: #This is an if true for testing, i will change the condition later
		if auth(session): #Check if the session is authentic
			command, *args = msg.split()
			return_value = {"type": command, "data": {}} #Parse commands
			if command == "history":
				time = int(args[1])
				try:
					data = get_history(args[0], time)
				except:
					return_value['type'] = 'redirect'
					return_value['data'] = {}
				else:
					return_value["data"] = data

			elif command == "update": #Send an update of the stock market
				try:
					value = get_current_value(args[0])
				except:
					return_value['type'] = 'redirect'
					return_value['data'] = {}
				else:
					return_value["data"] = value

			elif command == "name": #Send iformation of a symbol
				try:
					name = get_name(args[0])
				except:
					return_value['type'] = 'redirect'
					return_value['data'] = {}
				else:
					return_value["data"] = name

			elif command == "hotstocks": #Get a list of important stocks
				stocks = get_hot_stocks()
				return_value["data"] = stocks;

			elif command == "symbols": #Get list of all symbols.
				return_value["data"] = SYMBOLS

			send(return_value)
		else:
			send({"type": "unauth"})
	else:			
		send({"type": "error"})


@app.errorhandler(404)
def not_found(*args, **kwargs):
	return render_template("not_found.html") #Return not found page


@app.route("/account")
def account():
	if auth(session):
		return render_template("account.html") #If the user already logged go to account
	else:
		return redirect(url_for("landing")) #else go to landing


@app.route("/logout") #logout user
def logout():
	if auth(session):
		del ACTIVE_COOKIES[session["token"]]
		del session["user"]
		#del session["password"]
		del session["ip"]
		return render_template("login.html")

	else:
		return render_template("landing.html")


@app.route("/stocks/<code>")
def stock_table(code): #Get the information from any stock
	if auth(session):
		code = code.upper()
		
		return render_template("stock_table.html", code=code)

	else:
		abort(404)

@app.route("/buy", methods=["POST"])
def buy():
	if auth(session):
		if not request.form['buyquantity'].isnumeric():
			pass
		else:
			query = 'INSERT INTO `transactions` (`owner`, `originalprice`, `quantity`) VALUES (%s, %s, %s)'
			bought_quantity = int(request.form['buyquantity']) 
			original_price = get_current_value(request.form['stock']) * bought_quantity
			owner = ACTIVE_COOKIES[session['token']]['user']
			cursor = TOOLS["sql"].cursor()
			cursor.execute(query, (owner, original_price, bought_quantity))
			TOOLS["sql"].commit()


		return redirect("/stocks/{}".format(request.form['stock']))

	else:
		return redirect(url_for("landing"))

@app.route("/login", methods=["POST", "GET"])
def login(): #Login into the webpage
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
					token = generate_cookie(user, request.remote_addr)
					session["token"] = token
					session["user"] = user
					#session["password"] = "HAHA! there is no passwords stored in the cookies, dumbass"
					session["ip"] = request.remote_addr
					print(session)
					print(ACTIVE_COOKIES)
					return redirect(url_for("landing"))
		

	if not auth(session):
		return render_template("login.html")

	return redirect(url_for("landing"))


@app.route("/")
def landing():
	if auth(session): #If user is auth, go to logged.html
		return render_template("logged.html")

	else: #Else go to landing
		return render_template("landing.html")



app.run()