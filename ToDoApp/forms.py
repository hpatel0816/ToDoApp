from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo, ValidationError
from ToDoApp.models import User
import datetime

class SignUpForm(FlaskForm):
    #Validate username and email with specified length
    name = StringField('Name', validators=[DataRequired(), Length(min=6, max=25)])
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=80)])
    #Get password with specified length and ensure it mathces with confirm password field
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    #Complete signup form
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        #Check if username already exists in database and flash error
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        #Check if email already exists in database and flash error
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    #Get username and password
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    #Complete Login form
    submit = SubmitField('Login')


class TaskForm(FlaskForm):
    #Get task info
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=20)])
    category = StringField('Category', validators=[DataRequired(), Length(min=3, max=10)])
    deadline = DateField('Deadline', format='%Y-%m-%d', validators=[InputRequired()])
    description = StringField('Description', validators=[DataRequired(), Length(min=3, max=35)])
    #Complete add task form
    submit = SubmitField('Add Task')

    def validate_task_date(self):#Fix this to only accept valid dates
        currentDate = datetime.date.today()
        if self.deadline.data < currentDate.strftime("%Y-%m-%d"):
            raise ValidationError('The task timeline is invalid. Please try again.')