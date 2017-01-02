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

import psycopg2

# module
from secrets import secret

app = Flask(__name__)

from sqlalchemy import create_engine, desc, or_
from sqlalchemy.orm import sessionmaker
from database import Base, User, Word, Goal

engine = create_engine('postgresql://marco:marcopupu2014@localhost:5432/toddledatabase')
DBSession = sessionmaker(bind = engine)
session = DBSession()

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
	return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	# login  and signup page 
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
