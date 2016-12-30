from app import app, db, utils
from app.models import User, Post, Message
from flask import Flask, redirect, request
from flask_login import current_user
from flask_wtf import Form
from wtforms import validators, StringField, TextAreaField
from wtforms.validators import DataRequired
import time, datetime


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
        time.sleep(0.5)
        return redirect("/news")

    return utils.render_with_navbar("news/newpost.html", form=form, heading="News Item")

def new_message():
    form = NewPostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data

        newpost = Message(title=title, body=body, author=current_user.id, timestamp=datetime.datetime.now())
        db.session.add(newpost)
        db.session.commit()
        time.sleep(0.5)
        return redirect("/message")

    return utils.render_with_navbar("news/newpost.html", form=form, heading="Principal's Message")



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
        time.sleep(0.5)
        return redirect("/news?postid="+postid)

    return utils.render_with_navbar("news/editpost.html", form=form, title=title, body=body, heading="News Item")

def edit_message():
    postid = request.args.get("postid")
    if not postid: 
        return redirect("/newmessage")

    currentPost = Message.query.filter_by(id=postid).first()
    if not currentPost:
        return redirect("/newmessage")

    form = NewPostForm()

    title = currentPost.title
    body = currentPost.body

    if form.validate_on_submit():
        newtitle = form.title.data
        newbody = form.body.data
        currentPost.title = newtitle
        currentPost.body = newbody
        db.session.commit()
        time.sleep(0.5)
        return redirect("/messages?postid="+postid)

    return utils.render_with_navbar("news/editpost.html", form=form, title=title, body=body, heading="Principal's Message")


def delete_post():
    postid = request.args.get("postid")
    if not postid:
        return redirect("/news")

    post = Post.query.filter_by(id=postid)
    post.delete()
    db.session.commit()
    time.sleep(0.5)
    return redirect("/news")

def delete_message():
    postid = request.args.get("postid")
    if not postid:
        return redirect("/messages")

    post = Message.query.filter_by(id=postid)
    post.delete()
    db.session.commit()
    time.sleep(0.5)
    return redirect("/messages")
