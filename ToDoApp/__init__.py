from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from security import SECRET_KEY, DB_URI

app = Flask(__name__)

#Secret Key for server
app.config['SECRET_KEY'] = SECRET_KEY
#SQLAlchemy database path
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

#Create db
db = SQLAlchemy(app)
#Create bcrupt for password hashing
bcrypt = Bcrypt(app)
#Login manager to login users
loginManager = LoginManager(app)
loginManager.login_view = 'login'
loginManager.login_message_category = 'info'

from ToDoApp import routes