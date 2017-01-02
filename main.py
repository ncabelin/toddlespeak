# TO DO
# 1. Create User Login
# 2. Create User Signup
# 3. 

import random, string, datetime, os

# 3rd party dependencies
from flask import (Flask,
	render_template,
	request,
	url_for,
	redirect,
	flash,
	jsonify)
from flask_mail import Message, Mail

from flask import session as login_session
from flask import make_response
from itsdangerous import URLSafeSerializer
import bleach
from bcrypt import hashpw, checkpw, gensalt
from functools import wraps
import json
import re

# module
from secrets import secret

app = Flask(__name__)

from sqlalchemy import create_engine, desc, or_
from sqlalchemy.orm import sessionmaker
from database import Base, User, Word, Goal

engine = create_engine('postgresql://marco:marcopupu2014@localhost:5432/toddledatabase')
DBSession = sessionmaker(bind = engine)
session = DBSession()

def respond(msg, err):
	res = make_response(json.dumps(msg), err)
	res.headers['Content-Type'] = 'application/json'
	return res

def valid_username(username):
	if username and (len(username) < 30):
		return username
	else:
		return None

def valid_password(password):
	if password and (len(password) > 8):
		return password
	else:
		return None

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
	return email and EMAIL_RE.match(email)

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if 'username' in login_session:
			return f(*args, **kwargs)
		else:
			return redirect(url_for('login'))
	return decorated_function

@app.route('/', methods=['GET'])
def showHome():
	# homepage
	return render_template('home.html')

@app.route('/signup', methods=['POST'])
def signup():
	# signup
	username = request.form['username']
	password = request.form['password']
	verify = request.form['verify']
	email = request.form['email']
	t_name = request.form['t_name']
	month = request.form['month']
	day = request.form['day']
	year = request.form['year']

	# check if password and verify match
	if password != verify:
		return respond("Passwords don't match", 401)

	# check for duplicate username
	try:
		user = session.query(User).filter_by(username = username).one()
		if user:
			return respond('Username already taken', 401)
	except Exception as e:
		print(e)

	# check if username is below 30 characters
	username = valid_username(username)
	if not username:
		return respond('Invalid username, must be below 31 characters', 401)

	# check if password is not blank or below 8 characters
	password = valid_password(password)

	if password and valid_email(email) and t_name and month and day and year:
		newUser = User(
				username = username,
				registered_on = datetime.datetime.now().date(),
				password = hashpw(password.encode('utf-8'), gensalt()),
				email = email,
				t_name = t_name,
				t_birthday = datetime.date(int(year), int(month), int(day))
			)
		try:
			session.add(newUser)
			session.commit()
			return respond("Successfully signed up", 200)
		except Exception as e:
			print(e)
			return respond("Error saving", 401)
	return respond("Please make sure to fill up form correctly", 401)



@app.route('/login', methods=['GET', 'POST'])
def login():
	# login  and signup page 
	if request.method == 'POST':
		pass
	return render_template('login.html')

@app.route('/browse', methods=['GET'])
def browse():
	# main browsing page
	return render_template('browse.html')

@app.route('/summary', methods=['GET'])
def summary():
	return render_template('summary.html')

@app.route('/help', methods=['GET'])
def help():
	return render_template('help.html')


# Restful API Endpoints
# --------------------------
@app.route('/addword', methods=['POST'])
@login_required
def addWord():
	# add word
	return

@app.route('/getwords', methods=['GET'])
@login_required
def getWords():
	# get words in JSON format
	return

@app.route('/editword', methods=['POST'])
@login_required
def editWord():
	# edit word
	return

@app.route('/deleteword', methods=['DELETE'])
@login_required
def deleteWord():
	# delete word
	return

@app.route('/addgoal', methods=['GET','POST'])
@login_required
def addGoal():
	# add goal
	return

@app.route('/getgoals', methods=['GET','POST'])
@login_required
def getGoals():
	# get goals
	return

@app.route('/editgoal', methods=['GET','POST'])
@login_required
def editGoal():
	# edit goal
	return

if __name__ == '__main__':
	app.debug = True
	app.secret_key = secret()
	app.run(host='0.0.0.0', port=15000)
