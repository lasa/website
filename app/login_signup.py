from app import app, utils
from app.models import User
from flask import Flask, session, request, flash, url_for, redirect, \
    abort, g
from flask_login import login_user, logout_user, current_user, \
    login_required
from flask_wtf import Form
from wtforms import validators, StringField, PasswordField
from wtforms.validators import DataRequired
import bcrypt, hmac


class LoginForm(Form):
    username = StringField('Username:', validators=[validators.DataRequired(), validators.Length(min=4,max=16)])
    password = PasswordField('Password:', [
        validators.DataRequired(),
    ])


def generate_hash(password):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed


def check_password(candidate_password, pwhash):
    if (hmac.compare_digest(bcrypt.hashpw(candidate_password.encode("utf-8"), pwhash.encode("utf-8")), pwhash.encode("utf-8"))):
        return True
    else:
        return False

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
            del candidate_password
            return utils.render_with_navbar("login.html", form=form)
        else:
            if check_password(candidate_password, real_user.password):
                login_user(User.query.get(real_user.id))
                del candidate_password
                #if request.args.get('next') is None, redirect to /
                return redirect(request.args.get("next") if request.args.get("next") else "/")
            else:
                form.password.errors.append("Username and password do not match.")
                del candidate_password
                return utils.render_with_navbar("login.html", form=form)
    return utils.render_with_navbar("login.html", form=form)

def logout():
    logout_user()
    #if request.args.get('next') is None, redirect to /
    return redirect(request.args.get("next") if request.args.get("next") else "/")
