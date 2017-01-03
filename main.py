# ToddleSpeak

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

def find_user():
	try:
		user = session.query(User).filter_by(username = login_session['username']).one()
		return user
	except:
		return None

def find_user_logged():
	if 'username' in login_session:
		user = User(id = login_session['user_id'],
				username = login_session['username'],
				email = login_session['email']
			)
		return user
	else:
		return None

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
	return render_template('home.html', user_logged = find_user_logged())

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
		username = request.form['username']
		password = request.form['password']
		try:
			user = session.query(User).filter_by(username = username).one()
			hashed = user.password.encode('utf-8')
			if (hashpw(password.encode('utf-8'), 
				hashed) == hashed): # and (user.confirmed == True):
				login_session['user_id'] = user.id
				login_session['username'] = user.username
				login_session['email'] = user.password
				return respond("Successfully logged in", 200)
		except Exception as e:
			print(e)
		return respond("Invalid login", 401)
	return render_template('login.html', user_logged = find_user_logged())

@app.route('/logout', methods=['POST'])
@login_required
def logout():
	# Logout
	login_var = ['user_id', 'username', 'email']
	for l in login_var:
		del login_session[l]
	return respond('Successfully logged out', 200)

@app.route('/browse', methods=['GET'])
@login_required
def browse():
	# main browsing page
	return render_template('browse.html',
		user_logged = find_user_logged())

@app.route('/summary', methods=['GET'])
@login_required
def summary():
	return render_template('summary.html',
		user_logged = find_user_logged())

@app.route('/help', methods=['GET'])
def help():
	return render_template('help.html',
		user_logged = find_user_logged())


# Restful API Endpoints
# --------------------------
@app.route('/addword', methods=['POST'])
@login_required
def addWord():
	# add word
	user = find_user_logged()
	word = request.form['word']
	sound = request.form['sound']
	description = request.form['description']
	date_heard = datetime.datetime.now().date()
	newWord = Word(
			user_id = user.id,
			word = word,
			sound = sound,
			description = description,
			date_heard = date_heard
		)
	try:
		session.add(newWord)
		session.commit()
		return respond("Word Saved", 200)
	except Exception as e:
		print(e)
		return respond("Error saving", 401)

@app.route('/getwords', methods=['GET'])
@login_required
def getWords():
	# get words in JSON format
	try:
		words = session.query(Word).all()
	except:
		return respond("No words found", 401)
	if words:
		return jsonify(Words = [w.serialize for w in words])
	else:
		return respond("No words found", 401)

@app.route('/editword', methods=['POST'])
@login_required
def editWord():
	# edit word
	user = find_user_logged()
	return

@app.route('/deleteword', methods=['DELETE'])
@login_required
def deleteWord():
	# delete word
	return

@app.route('/addgoal', methods=['POST'])
@login_required
def addGoal():
	# add goal
	print(request.form.getlist('name[]'))
	user = find_user_logged()
	goal = request.form['goal']
	desc = request.form['description']
	newGoal = Goal(
			user_id = user.id,
			goal = goal,
			description = desc,
			date_created = datetime.datetime.now().date(),
			done = False
		)
	print('test')
	try:
		session.add(newGoal)
		session.commit()
		return respond("Added goal", 200)
	except Exception as e:
		print(e)
		return respond("Error saving goal", 401)

@app.route('/getgoals', methods=['GET'])
@login_required
def getGoals():
	# get goals
	user = find_user_logged()
	try:
		goals = session.query(Goal).filter_by(user_id = user.id).all()
		if goals:
			return jsonify(Goals = [g.serialize for g in goals])
		else:
			return respond("No goals found", 401)
	except Exception as e:
		print(e)
		return respond("Error getting goals", 401)

@app.route('/editgoal', methods=['GET','POST'])
@login_required
def editGoal():
	# edit goal
	return

if __name__ == '__main__':
	app.debug = True
	app.secret_key = secret()
	app.run(host='0.0.0.0', port=15000)
