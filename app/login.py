from app import app
from flask import render_template, redirect
from flask_wtf import Form
from wtforms import validators, StringField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField('Username:', validators=[validators.Length(min=4,max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=8,max=25)
    ])


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.username.data + " " + form.password.data)
        return redirect("/")
    return render_template("login.html", form=form)
