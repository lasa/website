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


def edit_page(page_name):
    if not page_name: 
        return render_template("404.html"), 404

    currentPage = Page.query.filter_by(name=page_name).first()
    if not currentPage:
        return render_template("404.html"), 404

    form = NewPageForm()

    title = currentPage.title
    bodyhtml = currentPage.body

    form.body.data = bodyhtml

    if form.validate_on_submit():
        newtitle = form.title.data
        newbody = form.bodyhtml.data
        newname = "-".join(newtitle.split(" ")).lower()
        currentPage.title = newtitle
        currentPage.body = newbody
        currentPage.name = newname
        db.session.commit()
        time.sleep(0.5)
        return redirect("/page/" + newname)

    return render_template("editpage.html", form=form, title=title, body=bodyhtml)


def delete_page(page_name):
    if not page_name:
        return render_template("404.html"), 404

    page = Page.query.filter_by(name=page_name)
    if not page:
        return render_template("404.html"), 404

    page.delete()
    db.session.commit()
    return redirect("/")

