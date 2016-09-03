from app import app, login_manager
from flask import render_template
from flask.ext.login import login_user, logout_user, current_user, \
    login_required


@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")


@app.route('/history/')
def history():
    return render_template("history.html")


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
