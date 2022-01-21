from ToDoApp import db, loginManager
from flask_login import UserMixin
import datetime


#Retrive user by id and login
@loginManager.user_loader
def loadUser(userId):
    return User.query.get(int(userId))

#User Table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f"User {self.id}, name: {self.name}, username: {self.username}, email: {self.email}."


#User Tasks Table
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(10), nullable=False)
    date_posted = db.Column(db.Date, nullable=False, default=datetime.date.today())
    deadline = db.Column(db.Date, nullable=False)
    date_completed = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(35), nullable=False)
    isComplete = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"Task {self.id}, user: {self.user}, title: {self.title}, deadline: {self.deadline}."