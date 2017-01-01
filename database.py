import os, sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	username = Column(String(250), nullable=False)
	registered_on = Column(Date, nullable=False)
	password = Column(String(250))
	email = Column(String(250), nullable=False)
	t_name = Column(String(250), nullable=False)
	t_birthday = Column(Date, nullable=False)
	confirmed = Column(Boolean(), default=False, nullable=False)
	words = relationship('Word', cascade='delete')
	goals = relationship('Goal', cascade='delete')

class Word(Base):
	__tablename__ = 'word'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)
	word = Column(String(250), nullable=False)
	sound = Column(String(250))
	description = Column(Text())
	date_heard = Column(Date, nullable=False)

	@property
	def serialize(self):
		return {
			'word_id': self.id,
			'user_id': self.user_id,
			'word': self.word,
			'sound': self.sound,
			'description': self.description,
			'date_heard': self.date_heard
		}

class Goal(Base):
	__tablename__ = 'goal'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)
	goal = Column(String(500))
	description = Column(Text())
	date_created = Column(Date, nullable=False)
	date_modified = Column(Date)
	date_reached = Column(Date)
	done = Column(Boolean() default=False, nullable=False)

	@property
	def serialize(self):
		return {
			'goal_id': self.id,
			'goal': self.goal,
			'description': self.description,
			'date_created': self.date_created,
			'date_modified': self.date_modified,
			'date_reached': self.date_reached,
			'done': self.done 
		}

engine = create_engine('postgresql://marco:marcopupu2014@localhost:5432/toddledatabase')
Base.metadata.create_all(engine)