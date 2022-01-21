from flask import Flask, redirect, url_for, render_template, request, flash
from ToDoApp import app, db, bcrypt
from ToDoApp.forms import TaskForm, SignUpForm, LoginForm
from ToDoApp.models import User, Task
from flask_login import login_user, current_user, logout_user, login_required
import datetime
import requests


@app.route('/')
@app.route('/main')
def mainPage():
    return render_template("index.html", title='Main')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    #Redirect logged in user to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    #Render signup form
    form = SignUpForm()

    #Validate form submission
    if request.method == 'POST' and form.validate_on_submit():
        #Generate hashed password
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #Create new user and add to database
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hashedPassword)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. Please login to continue.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    #Redirect logged in user to home page
    if current_user.is_authenticated:
       return redirect(url_for('home'))
    #Render login form
    form = LoginForm()

    #Validate form submission
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        #Check if user exists in database and entered password is correct
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            #Redirect to next requested url or to home page
            nextPage = request.args.get('next')
            if nextPage:
                return redirect(nextPage)
            else:
               return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username or password.', 'danger')
    
    return render_template('login.html', title='Login', form=form)


@app.route('/home')
@login_required
def home():
    #Get number of completed vs non-completed tasks and list of upcoming tasks
    completedTasks = Task.query.filter_by(user=current_user.username, isComplete=True).count()
    pendingTasks = Task.query.filter_by(user=current_user.username, isComplete=False).count()
    upcomingTasks = Task.query.filter_by(user=current_user.username, isComplete=False)

    #Fetch a random quote from quote generator api
    url = f'https://zenquotes.io/api/random'
    r = requests.get(url)
    quote = r.json()

    return render_template('home.html', title='Home', pendingTasks=pendingTasks, completedTasks=completedTasks, upcomingTasks=upcomingTasks, quote=quote)


@app.route('/addTask', methods=['GET', 'POST'])
@login_required
def addTask():
    #Render task form
    form = TaskForm()   

    #Validate form submission
    if request.method == 'POST' and form.validate_on_submit():
        #Create new task and add to database
        task = Task(user=current_user.username, title= form.title.data, category=form.category.data, deadline=form.deadline.data, date_completed=form.deadline.data, description=form.description.data)
        db.session.add(task)
        db.session.commit()
        flash('Your task has been created.', 'success')
        return redirect(url_for('taskList'))

    return render_template('addTask.html', title='Add Task', form=form, legend='Create Task')


@app.route('/tasklist', methods=['GET', 'POST'])
@login_required
def taskList():
    #Get tasks for current user
    userTasks = Task.query.filter_by(user=current_user.username, isComplete=False)
    #Filter for unique catgories
    categories = set()
    for task in userTasks:
        categories.add(task.category)

    #Match colours to categories
    colours = ['#F72585', '#B5179E', '#7209B7', '#560BAD', '#480CA8', '#3A0CA3', '#3F37C9', '#4361EE', '#4895EF', '#4CC9F0']
    taskCategories = {}
    for i, category in enumerate(categories):
        taskCategories[category] = colours[i]

    return render_template('taskList.html', title='Task List', tasks=userTasks, categories=taskCategories)


@app.route('/complete/<int:taskId>', methods=['GET', 'POST'])
@login_required
def complete(taskId):
    #Query for selected task
    task = Task.query.get(taskId)
    #Mark as completed and update its completion date
    task.isComplete = True
    dateCompleted = datetime.date.today()
    task.date_completed = dateCompleted
    db.session.commit()
    flash('The task is marked as complete.', 'success')
    return redirect(url_for('taskList'))


@app.route('/update/<int:taskId>', methods=['GET', 'POST'])
@login_required
def updateTask(taskId):
    #Query for selected task
    task = Task.query.get(taskId)
    form = TaskForm()

    #Update task properties and add to database
    if request.method == 'POST' and form.validate_on_submit():
        task.title = form.title.data
        task.category = form.category.data
        task.deadline = form.deadline.data
        task.date_completed = form.deadline.data
        task.description = form.description.data
        db.session.commit()
        flash('Your task has been updated.', 'success')
        return redirect(url_for('taskList'))
    #Display current task properties
    elif request.method == 'GET':
        form.title.data = task.title
        form.category.data = task.category
        form.deadline.data = task.deadline
        form.description.data = task.description
        form.submit.label.text = 'Update Task'

    return render_template('addTask.html', title='Update Task', form=form, legend='Update Task')


@app.route('/delete/<int:taskId>', methods=['GET', 'POST'])
@login_required
def delete(taskId):
    #Query for selected task
    task = Task.query.get(taskId)
    #Remove task from database
    db.session.delete(task)
    db.session.commit()
    flash('Your task has been deleted.', 'success')
    return redirect(url_for('taskList'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('mainPage'))