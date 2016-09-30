from app import app, db
from app.models import User, Post
from flask import Flask, redirect, render_template, request
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
        return redirect("/news")

    return render_template("newpost.html", form=form)

def edit_post():
    postid = request.args.get("postid")
    if not postid: 
        return redirect("/newpost")

    currentPost = Post.query.filter_by(id=postid).first()
    if not currentPost:
        return redirect("/newpost")

    form = NewPostForm()

    title = currentPost.title
    body = currentPost.body

    if form.validate_on_submit():
        newtitle = form.title.data
        newbody = form.body.data
        currentPost.title = newtitle
        currentPost.body = newbody
        db.session.commit()
        return redirect("/news?postid="+postid)

    return render_template("editpost.html", form=form, title=title, body=body)

def delete_post():
    postid = request.args.get("postid")
    if not postid:
        return redirect("/news")

    post = Post.query.filter_by(id=postid)
    post.delete()
    db.session.commit()
    return redirect("/news")
