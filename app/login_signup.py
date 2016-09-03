from app import app
from flask import render_template, redirect
from flask_wtf import Form
from wtforms import validators, StringField, PasswordField
from wtforms.validators import DataRequired
import bcrypt, hmac


class SignupForm(Form):
    username = StringField('Username:', validators=[validators.Length(min=4,max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=8,max=25),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField("Confirm Password")

    
class LoginForm(Form):
    username = StringField('Username:', validators=[validators.Length(min=4,max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=8,max=25)
    ])


def generate_hash(password):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed

def check_password(candidate_password, pwhash):
    if (hmac.compare_digest(bcrypt.hashpw(candidate_password.encode("utf-8"), pwhash), pwhash)):
        return True
    else:
        return False

def signup():
    form = SignupForm()
    if form.validate_on_submit():
        print(form.username.data + " " + form.password.data)
        return redirect("/login/")
    return render_template("signup.html", form=form)


def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = generate_hash("hello123") #replace this with getting hashed PW from database
        candidate = form.password.data
        print(check_password(candidate, password)) #replace this with using flask-login to login user if check_password is True
        return redirect("/")
    return render_template("login.html", form=form)
