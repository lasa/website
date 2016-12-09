from app import app, db
from app.models import User, Page
from flask import Flask, redirect, render_template, request
from flask_login import current_user
from flask_wtf import Form
from wtforms import validators, StringField, TextAreaField, HiddenField
from wtforms.validators import DataRequired
import datetime, time

#custom widget for rendering a QuillJS input
def QuillJS(field):
    return """  <link href="https://cdn.quilljs.com/1.1.6/quill.snow.css" rel="stylesheet">
                <div id="editor">
                %s
                </div>
                <script src="https://cdn.quilljs.com/1.1.6/quill.js"></script>
                <script>
                  var quill = new Quill('#editor', {
                    theme: 'snow'
                  });
                </script> """ % field._value()

class NewPageForm(Form):
    title = StringField('Title:', validators=[validators.DataRequired(), validators.Length(min=0,max=1000)])
    body = TextAreaField('Body:', validators=[validators.Length(min=0,max=75000)], widget=QuillJS)
    bodyhtml = HiddenField();


def new_page():
    form = NewPageForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.bodyhtml.data

        name = "-".join(title.split(" ")).lower()

        newpage = Page(title=title, name=name, body=body)
        db.session.add(newpage)
        db.session.commit()
        time.sleep(0.5);
        return redirect("/page/" + name)

    return render_template("newpage.html", form=form)


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

    return render_template("news/editpost.html", form=form, title=title, body=body, heading="News Item")


def delete_post():
    postid = request.args.get("postid")
    if not postid:
        return redirect("/news")

    post = Post.query.filter_by(id=postid)
    post.delete()
    db.session.commit()
    return redirect("/news")

