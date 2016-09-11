from app import app, login_signup, models, login_manager
from app.models import User
from flask import render_template

@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")

@app.route('/history/')
def history():
    return render_template("history.html")

@app.route('/profile/')
def profile():
    return render_template("profile.html")

@app.route('/accolades/')
def accolades():
    return render_template("accolades.html")

@app.route('/contact/')
def contact():
    return render_template("contact.html")

@app.route('/mission/')
@app.route('/vision/')
def mission():
    return render_template("mission.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    return login_signup.login()

@app.route("/logout/", methods=["GET", "POST"])
def logout():
    return login_signup.logout()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
