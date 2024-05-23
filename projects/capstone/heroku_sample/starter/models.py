import os
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Person
Have title and release yea

TODO: Two classes with primary keys at at least two attributes each
[Optional but encouraged] One-to-many or many-to-many relationships between classes
'''

  #  Got reminder about join tables from here: https://medium.com/@beckerjustin3537/creating-a-many-to-many-relationship-with-flask-sqlalchemy-69018d467d36

person_movie = db.Table(
  'person_movie',
  db.Column('people_id', db.Integer, db.ForeignKey('People.id')),
  db.Column('movies_id', db.Integer, db.ForeignKey('Movies.id'))
)

class Person(db.Model):  
  __tablename__ = 'People'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String)
  catchphrase = db.Column(db.String)
  age = db.Column(db.Integer)
  gender = db.Column(db.String)
  movies = db.relationship('Movies', secondary='person_movie', back_populates='person')

  def __init__(self, name, age, gender, catchphrase=""):
    self.name = name
    self.catchphrase = catchphrase
    self.age = age
    self.gender = gender

  
  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender,
      'catchphrase': self.catchphrase}

class Movies(db.Model):
    __tablename__ = 'Movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    person = db.relationship('Person', secondary='person_movie', back_populates='movies')

    def __init__(self, title, release_date):
      self.title = title
      self.release_date = release_date

    def insert(self):
       db.session.add(self)
       db.session.commit()
  
    def update(self):
       db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def format(self):
      return {
        'id': self.id,
        'title': self.title,
        'release_date': self.release_date}

