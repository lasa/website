from app import app
from app.models import User
from flask import Flask, session, request, flash, url_for, redirect, \
    render_template, abort, g
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from flask_wtf import Form
from wtforms import validators, StringField, PasswordField
from wtforms.validators import DataRequired
import bcrypt, hmac

    
class LoginForm(Form):
    username = StringField('Username:', validators=[validators.Length(min=4,max=16)])
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


def login():
    form = LoginForm()
    if form.validate_on_submit():
        candidate_username = form.username.data
        candidate_password = form.password.data
        real_user = User.query.filter_by(name=candidate_username).first().id
        if real_user is None:
            return render_template("login.html", form=form, login_error="Incorrect user")
        else:
            if check_password(candidate_password, User.query.get(real_user).password):
                login_user(User.query.get(real_user))
                return redirect("/")
            else:
                return render_template("login.html", form=form, login_error="Incorrect password")
    return render_template("login.html", form=form)

def logout():
    logout_user()
    return redirect("/")
