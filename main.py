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

import psycopg2

# module
from secrets import secret

app = Flask(__name__)

from sqlalchemy import create_engine, desc, or_
from sqlalchemy.orm import sessionmaker
from database import Base, User, Word, Goals

engine = create_engine('postgresql://marco:marcopupu2014@localhost:5432/toddledatabase')
DBSession = sessionmaker(bind = engine)
session = DBSession()

def find_word():
	# find word
	return

@app.route('/', methods=['GET'])
def showHome():
	# homepage
	return

@app.route('/signup', methods=['GET', 'POST'])
	# signup
	return

@app.route('/login', methods=['GET', 'POST'])
def login():
	# login page
	return

@app.route('/addword', methods=['POST'])
def addWord():
	# add word
	return

@app.route('/getwords', methods=['GET'])
def getWords():
	# get words in JSON format
	return

@app.route('/editword', methods=['GET'])
def editWord():
	# edit word
	return

@app.route('/deleteword', methods=['DELETE'])
def deleteWord():
	# delete word
	return

@app.route('/addgoal', methods=['GET','POST'])
def addGoal():
	# add goal
	return

@app.route('/getgoals', methods=['GET','POST'])
def getGoals():
	# get goals
	return

@app.route('/editgoal', methods=['GET','POST'])
def editGoal():
	# edit goal
	return

if __name__ == '__main__':
	app.debug = True
	app.secret_key = secret()
	app.run(host='0.0.0.0', port=15000)
