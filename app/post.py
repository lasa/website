from app import app, db
from app.models import User, Post
from flask import Flask, redirect, render_template
from flask_login import current_user
from flask_wtf import Form
from wtforms import validators, StringField, TextAreaField
from wtforms.validators import DataRequired
import datetime


class NewPostForm(Form):
    title = StringField('Title:', validators=[validators.DataRequired(), validators.Length(min=0,max=1000)])
    body = TextAreaField('Body:')


def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data

        newpost = Post(title=title, body=body, author=current_user.id, timestamp=datetime.datetime.now())
        db.session.add(newpost)
        db.session.commit()
        return redirect("/")

    return render_template("newpost.html", form=form)
