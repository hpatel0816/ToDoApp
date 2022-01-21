from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 

app = Flask(__name__)

#Secret Key for server
app.config['SECRET_KEY'] = 'hyy6749kj9014hbshy8livc11h74gst5'
#SQLAlchemy database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appDatabase.db'

#Create db
db = SQLAlchemy(app)
#Create bcrupt for password hashing
bcrypt = Bcrypt(app)
#Login manager to login users
loginManager = LoginManager(app)
loginManager.login_view = 'login'
loginManager.login_message_category = 'info'

from ToDoApp import routes