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
	if (not "token" in session) or (not "user" in session):
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
					return_value['symbol'] = args[0]

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
		cursor = TOOLS["sql"].cursor()
		query = 'SELECT money FROM users WHERE username=%s'

		user = ACTIVE_COOKIES[session['token']]['user']

		cursor.execute(query, (user,))

		money = cursor.fetchall()[0][0]

		return render_template("account.html",user=user, money=money) #If the user already logged go to account
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
			query = 'INSERT INTO `transactions` (`owner`, `originalprice`, `quantity`, `symbol`,`total_price`) VALUES (%s, %s, %s, %s,%s)'
			bought_quantity = int(request.form['buyquantity']) 
			original_price = get_current_value(request.form['stock']) 
			total_price = bought_quantity * original_price
			owner = ACTIVE_COOKIES[session['token']]['user']
			cursor = TOOLS["sql"].cursor()
			
			#Get user data

			user_data = "SELECT money FROM users WHERE username=%s"
			cursor.execute(user_data, (owner,))
			money = cursor.fetchall()[0][0]

			if total_price > money:
				return redirect("/stocks/{}".format(request.form['stock']))

			money -= total_price
			substract_money = '''UPDATE users
			SET money=%s
			WHERE username=%s'''

			cursor.execute(substract_money, (money, owner))
			cursor.execute(query, (owner, original_price, bought_quantity, request.form['stock'],total_price))
			TOOLS["sql"].commit()


		return redirect("/stocks/{}".format(request.form['stock']))

	else:
		return redirect(url_for("landing"))


@app.route("/sell", methods=["POST"])
def sell():
	if auth(session):
		if request.form['sellshare'].isnumeric():
			quantity = int(request.form['sellshare'])
			if quantity > 0:
				stock = request.form['stock']
				date = request.form['date']
				cursor = TOOLS["sql"].cursor()
				name = ACTIVE_COOKIES[session['token']]['user']
				query = "UPDATE transactions SET quantity=%s, total_price=%s WHERE owner=%s AND purchase_date=%s AND symbol=%s"
				moneney_query = "UPDATE users SET money=%s WHERE username=%s"
				fetch_query = "SELECT quantity, total_price, originalprice FROM transactions WHERE owner=%s AND purchase_date=%s AND symbol=%s"
				current_money = "SELECT money FROM users WHERE username=%s"

				cursor.execute(current_money, (name,))
				old_money = cursor.fetchall()[0][0]

				cursor.execute(fetch_query, (name ,date, stock))
				old_qty, old_price, original_price = cursor.fetchall()[0]
				a_current_value = get_current_value(stock)
				new_qty = old_qty - quantity
				new_total_price = (original_price * quantity) 
				earned = (a_current_value * quantity) 
				new_total_money = old_money + earned

				earned_two = earned - (original_price * quantity)

				print("New total acc: {}".format(new_total_money))
				print("New qty: {}".format(new_qty))
				print("New total invest: {}".format(new_total_price))
				print("Earned: {}".format(earned))

				if new_qty < 0:
					return redirect("/portfolio")
				elif new_qty == 0:
					query = "DELETE FROM transactions WHERE owner=%s AND purchase_date=%s AND symbol=%s"
					cursor.execute(query, (name, date, stock))

				else:
					cursor.execute(query, (new_qty, new_total_price, name, date, stock))

				cursor.execute(moneney_query, (new_total_money, name))							
				update_history = "INSERT INTO history(`user`, `symbol`, `quantity`, `sell_price`, `earnings`, `bought_price`) VALUES (%s, %s, %s, %s, %s, %s) "

				cursor.execute(update_history, (name, stock, quantity, a_current_value, earned_two, original_price))

				update_trans = ""
				if earned_two > 0:
					update_trans = "UPDATE users SET positive_transactions=positive_transactions+1 WHERE username=%s"
				elif earned_two < 0 :
					update_trans = "UPDATE users SET negative_transactions=negative_transactions+1 WHERE username=%s"
				
				if len(update_trans):
					cursor.execute(update_query, (name, ))

				TOOLS["sql"].commit()

		else:
			pass
		
		return redirect("/portfolio")



	else:
		return redirect(url_for("landing"))



@app.route("/history")
def history():
	if auth(session):

		#history = [['GME', 1, 10, 1000, 10]]

		cursor = TOOLS['sql'].cursor()
		username = ACTIVE_COOKIES[session['token']]['user']
		query = 'SELECT symbol, bought_price, quantity, earnings, sell_price FROM history WHERE user=%s'
		cursor.execute(query, (username,))
		history = cursor.fetchall()
		return render_template("history.html", history=history)

	else:
		return redirect("/")

@app.route("/portfolio")
def portfolio():
	if auth(session):

		portfolio = []#[{'symbol': 'GME', "boughtprice": 1, "quantity": 10000, 'name': get_name('GME'), 'date': date }]


		cursor = TOOLS["sql"].cursor()
		query = "SELECT symbol, originalprice, quantity, purchase_date, total_price FROM transactions WHERE owner=%s"
		user = ACTIVE_COOKIES[session['token']]['user']

		cursor.execute(query, (user,))
		portfolio_items = cursor.fetchall()
		total_investment = 0
		earnings = 0
		final_current_value = 0
		for item in portfolio_items:
			data = {}
			data['symbol'] = item[0]
			data['boughtprice'] =  item[1]
			data['quantity'] = item[2]
			data['date'] = item[3]
			data['name'] = get_name(data['symbol'])
			total_current_value = get_current_value(data['symbol']) * data['quantity']
			data['earnings'] =  float("{:.2f}".format(total_current_value - item[4]))
			portfolio.append(data)

			#Add to totals
			total_investment += item[4]
			final_current_value += total_current_value
			earnings += data['earnings']

		total_investment = float("{:.2f}".format(total_investment))
		final_current_value = float("{:.2f}".format(final_current_value))
		earnings = float("{:.2f}".format(earnings))


		return render_template("portfolio.html", total_invested=total_investment, current_value=final_current_value, earnings=earnings, portfolio = portfolio)

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