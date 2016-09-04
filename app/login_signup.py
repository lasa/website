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
import sys
import ctypes


class LoginForm(Form):
    username = StringField('Username:', validators=[validators.DataRequired(), validators.Length(min=4,max=16)])
    password = PasswordField('Password:', [
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


def overwrite_password(string):
    location = id(string) + 20
    size = sys.getsizeof(string) - 20
    # change the "6" to whatever is on the actual system
    memset = ctypes.CDLL("libc.so.6").memset
    print("Clearing 0x%08x size %i bytes" % (location, size))
    memset(location, 0, size)


def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        candidate_username = form.username.data
        candidate_password = form.password.data
        real_user = User.query.filter_by(name=candidate_username).first()
        if real_user is None:
            form.username.errors.append("Username does not exist.")
            overwrite_password(candidate_password)
            del candidate_password
            return render_template("login.html", form=form)
        else:
            if check_password(candidate_password, real_user.password):
                login_user(User.query.get(real_user.id))
                overwrite_password(candidate_password)
                del candidate_password
                return redirect("/")
            else:
                form.password.errors.append("Username and password do not match.")
                overwrite_password(candidate_password)
                del candidate_password
                return render_template("login.html", form=form)
    return render_template("login.html", form=form)


def logout():
    logout_user()
    return redirect("/")
