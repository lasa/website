from app import app, db, utils
from app.models import User, Link
from flask import Flask, redirect, request
from flask_login import current_user
from flask_wtf import Form
from wtforms import validators, StringField, SelectField, BooleanField
from flask_wtf.html5 import IntegerField
from wtforms.validators import DataRequired
import os, time

choices = [('calendars', 'Calendars'),
                ('about', 'About Us'),
                ('academics', 'Academics'),
                ('students', 'Students'),
                ('parents', 'Parents'),
                ('admissions', 'Admissions')]

def generate_link_list():
    uploads = os.listdir(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']))
    uploads.remove(".gitignore")
    link_list = [('none', '')]
    image_extensions = ["png", "jpg", "jpeg", "gif", "bmp"]
    for upload in uploads:
        if not ('.' in upload and upload.rsplit('.', 1)[1].lower() in image_extensions):
            link_list.append(('/uploads/' + upload, upload))
    return link_list

   
class NewLinkForm(Form):
    title = StringField('Title:', validators=[validators.InputRequired(), validators.Length(min=0,max=1000)])
    category = SelectField('Category:', choices=choices)
    dividerBelow = BooleanField('Divider below link in dropdown menu')
    index = IntegerField('Ordering index (lower number = higher up in dropdown menu):', validators=[validators.InputRequired()])

    websiteregex = r'((http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&/=]*))|\/[-a-zA-Z0-9@:%_\+.~#?&/=]*'
    link_list = SelectField('Choose from uploads: ', choices=generate_link_list())
    url = StringField('URL (external link or relative path): ', validators=[validators.InputRequired(), validators.Regexp(websiteregex, message="Invalid URL. Must be a valid external link or a relative URL beginning with '/'."), validators.Length(min=0,max=50)])


def new_link():
    form = NewLinkForm()
    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        dividerBelow = form.dividerBelow.data
        index = form.index.data
        url = form.url.data

        if not (url.startswith('/')  or url.startswith("http://") or url.startswith("https://")):
            url = "http://" + url

        if index and (index<0 or index>100):
            form.index.errors.append("Number must be between 0 and 100.")
            return utils.render_with_navbar("newlink.html", form=form, title=title, index=index, url=url)

        newlink = Link(title=title, index=index, category=category, dividerBelow=dividerBelow, url=url)
        db.session.add(newlink)
        db.session.commit()
        time.sleep(0.5)
        return redirect("/links")

    return utils.render_with_navbar("newlink.html", form=form)

def edit_link():
    linkid = request.args.get("id")
    if not linkid: 
        return redirect("/newlink")

    currentLink = Link.query.filter_by(id=linkid).first()
    if not currentLink:
        return redirect("/newlink")

    title = currentLink.title
    category = currentLink.category
    dividerBelow = currentLink.dividerBelow
    index = currentLink.index
    url = currentLink.url

    form = NewLinkForm(category=category, dividerBelow=dividerBelow)

    if form.validate_on_submit():
        newtitle = form.title.data
        newcategory = form.category.data
        newdividerBelow = form.dividerBelow.data
        newindex = form.index.data
        newurl = form.url.data

        if not (newurl.startswith('/')  or newurl.startswith("http://") or newurl.startswith("https://")):
            newurl = "http://" + newurl

        if newindex and (newindex<0 or newindex>100):
            form.newindex.errors.append("Number must be between 0 and 100.")
            return utils.render_with_navbar("editlink.html", form=form, title=newtitle, index=newindex, url=newurl)


        currentLink.title = newtitle
        currentLink.category = newcategory
        currentLink.dividerBelow = newdividerBelow
        currentLink.index = newindex
        currentLink.url = newurl

        db.session.commit()
        time.sleep(0.5)
        return redirect("/links")

    return utils.render_with_navbar("editlink.html", form=form, title=title, index=index, url=url)

def delete_link():
    linkid = request.args.get("id")
    if not linkid:
        return redirect("/links")

    link = Link.query.filter_by(id=linkid)
    link.delete()
    db.session.commit()
    time.sleep(0.5)
    return redirect("/links")
