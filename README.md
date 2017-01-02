# Toddlespeak

## Synopsis

This app provides an interface for recording any toddler's words and phrases. It provides counters for each progress. Every word / phrase can be saved to a database with the word/phrase, its equivalent sound, date heard, with a description for every word/phrase. This will help visualize through graphs, and tables, and determine how the child is progressing through his/her speech development. You can easily collaborate with the speech therapist by giving them account credentials.

## Motivation

Monitoring your toddler's speech can be hard. This app simplifies the ability to save progress on a daily basis and keep counts and reminders of what to practice / goals for the therapy.

## Code Features
1. Python
2. Flask, PostgreSQL, psycopg2
3. jQuery
4. Bootstrap
5. D3.js

## Tables
1. User
		0. id
		a. username - str(250)
		b. registered_on - datetime
		c. password - str()
		d. email - str(250)
		e. t_name - str(), required
		f. t_birthday - str(), required
		g. confirmed - boolean

2. Word
		0. id
		a. user_id - int
		b. word - str(500)
		c. sound - str(500)
		d. description - str(500)
		e. date_heard - date

3. Goals
		0. id
		a. user_id - int
		b. goal - str(500)
		c. comment - str()
		d. date_created
		e. date_modified
		f. date_reached
		g. done

## Installation
Make sure to check for or install these dependencies, (through Virtualenv)
1. flask
2. bcrypt
3. flask_mail
4. requests
5. bleach


## Future Features
1. ReactJS web framework
2. React Native (iOS app, Android app)

## Contributors

Neptune Michael Cabelin

## License

MIT