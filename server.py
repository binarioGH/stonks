#-*-coding: utf-8-*-
from flask import Flask, render_template, request, session, abort
from flask_socketio import SocketIO, send
from markupsafe import escape


CODES = ["GME"]




app = Flask(__name__)
socketio = SocketIO(app)


@app.errorhandler(404)
def not_found(*args, **kwargs):
	return render_template("not_found.html")

@app.route("/stocks/<code>")
def stock_table(code):
	code = code.upper()

	if code in CODES:
		return render_template("stock_table.html", code=code)

	abort(404)



app.run()