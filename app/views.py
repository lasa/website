from app import app, login_manager, login_signup
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

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    return login_signup.signup()

@app.route("/login/", methods=["GET", "POST"])
def login():
    return login_signup.login()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404