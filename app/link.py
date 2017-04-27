import os
import time

from app import app, db, utils
from app.models import Link
from flask import redirect, request
from flask_wtf import Form
from flask_wtf.html5 import IntegerField
from wtforms import validators, StringField, SelectField, BooleanField

CHOICES = [('calendars', 'Calendars'),
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
    title = StringField('Title:', validators=[validators.InputRequired(), validators.Length(min=0, max=1000)])
    category = SelectField('Category:', choices=CHOICES)
    divider_below = BooleanField('Divider below link in dropdown menu')
    index = IntegerField('Ordering index (lower number = higher up in dropdown menu):', validators=[validators.InputRequired()])

    websiteregex = r'((http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&/=]*))|\/[-a-zA-Z0-9@:%_\+.~#?&/=]*'
    link_list = SelectField('Choose from uploads: ', choices=generate_link_list())
    url = StringField('URL (external link or relative path): ', validators=[validators.InputRequired(), validators.Regexp(websiteregex, message="Invalid URL. Must be a valid external link or a relative URL beginning with '/'."), validators.Length(min=0, max=50)])


def new_link():
    form = NewLinkForm()
    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        divider_below = form.divider_below.data
        index = form.index.data
        url = form.url.data

        if not (url.startswith('/')  or url.startswith("http://") or url.startswith("https://")):
            url = "http://" + url

        if index and (index < 0 or index > 100):
            form.index.errors.append("Number must be between 0 and 100.")
            return utils.render_with_navbar("newlink.html", form=form, title=title, index=index, url=url)

        newlink = Link(title=title, index=index, category=category, divider_below=divider_below, url=url)
        db.session.add(newlink)
        db.session.commit()
        time.sleep(0.5)
        return redirect("/links")

    return utils.render_with_navbar("newlink.html", form=form)

def edit_link():
    linkid = request.args.get("id")
    if not linkid:
        return redirect("/newlink")

    current_link = Link.query.filter_by(id_=linkid).first()
    if not current_link:
        return redirect("/newlink")

    title = current_link.title
    category = current_link.category
    divider_below = current_link.divider_below
    index = current_link.index
    url = current_link.url

    form = NewLinkForm(category=category, divider_below=divider_below)

    if form.validate_on_submit():
        newtitle = form.title.data
        newcategory = form.category.data
        new_divider_below = form.divider_below.data
        newindex = form.index.data
        newurl = form.url.data

        if not (newurl.startswith('/')  or newurl.startswith("http://") or newurl.startswith("https://")):
            newurl = "http://" + newurl

        if newindex and (newindex < 0 or newindex > 100):
            form.newindex.errors.append("Number must be between 0 and 100.")
            return utils.render_with_navbar("editlink.html", form=form, title=newtitle, index=newindex, url=newurl)


        current_link.title = newtitle
        current_link.category = newcategory
        current_link.divider_below = new_divider_below
        current_link.index = newindex
        current_link.url = newurl

        db.session.commit()
        time.sleep(0.5)
        return redirect("/links")

    return utils.render_with_navbar("editlink.html", form=form, title=title, index=index, url=url)

def delete_link():
    linkid = request.args.get("id")
    if not linkid:
        return redirect("/links")

    link = Link.query.filter_by(id_=linkid)
    link.delete()
    db.session.commit()
    time.sleep(0.5)
    return redirect("/links")
