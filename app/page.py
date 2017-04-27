import time

from app import db, utils
from app.models import Page
from flask import redirect
from flask_wtf import Form
from flask_wtf.html5 import IntegerField
from wtforms import validators, StringField, TextAreaField, HiddenField, SelectField, BooleanField

CHOICES = [('none', 'None (hidden)'),
           ('calendars', 'Calendars'),
           ('about', 'About Us'),
           ('academics', 'Academics'),
           ('students', 'Students'),
           ('parents', 'Parents'),
           ('admissions', 'Admissions')]

class NewPageForm(Form):
    title = StringField('Title:', validators=[validators.Length(min=0, max=1000)])
    category = SelectField('Category:', choices=CHOICES)
    divider_below = BooleanField('Divider below page name in dropdown menu')
    index = IntegerField('Ordering index (lower number = higher up in dropdown menu):', validators=[validators.InputRequired()])
    body = TextAreaField('Body:', validators=[validators.Length(min=0, max=75000)], widget=utils.TinyMCE)
    bodyhtml = HiddenField()


def new_page():
    form = NewPageForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.bodyhtml.data
        category = form.category.data
        divider_below = form.divider_below.data
        index = form.index.data

        if len(title) < 1:
            form.title.errors.append("This field is required.")
            form.body.data = body
            return utils.render_with_navbar("newpage.html", form=form, title=title, index=index)

        if index and (index < 0 or index > 100):
            form.index.errors.append("Number must be between 0 and 100.")
            form.body.data = body
            return utils.render_with_navbar("newpage.html", form=form, title=title, index=index)

        name = "-".join(title.split(" ")).lower()

        page = Page.query.filter_by(name=name).first()
        if page:
            form.title.errors.append("A page with this name already exists.")
            form.body.data = body
            return utils.render_with_navbar("newpage.html", form=form, title=title, index=index)


        newpage = Page(title=title, name=name, category=category, divider_below=divider_below, index=index, body=body)
        db.session.add(newpage)
        db.session.commit()
        time.sleep(0.5)
        return redirect("/page/" + name)

    return utils.render_with_navbar("newpage.html", form=form)


def edit_page(page_name):
    if not page_name:
        return utils.render_with_navbar("404.html"), 404

    current_page = Page.query.filter_by(name=page_name).first()
    if not current_page:
        return utils.render_with_navbar("404.html"), 404


    title = current_page.title
    bodyhtml = current_page.body
    category = current_page.category
    divider_below = current_page.divider_below
    index = current_page.index

    form = NewPageForm(category=category, divider_below=divider_below)

    form.body.data = bodyhtml

    if form.validate_on_submit():
        newtitle = form.title.data
        newbody = form.bodyhtml.data
        newcategory = form.category.data
        new_divider_below = form.divider_below.data
        newindex = form.index.data

        if len(newtitle) < 1:
            form.title.errors.append("This field is required.")
            form.body.data = newbody
            return utils.render_with_navbar("editpage.html", form=form, title=newtitle, index=newindex)

        if index and (index < 0 or index > 100):
            form.index.erros.append("Number must be between 0 and 100.")
            form.body.data = newbody
            return utils.render_with_navbar("editpage.html", form=form, title=newtitle, index=newindex)

        newname = "-".join(newtitle.split(" ")).lower()

        if newname != page_name:
            page = Page.query.filter_by(name=newname).first()
            if page:
                form.title.errors.append("A page with this name already exists.")
                form.body.data = newbody
                return utils.render_with_navbar("editpage.html", form=form, title=newtitle, index=newindex)

        current_page.title = newtitle
        current_page.body = newbody
        current_page.name = newname
        current_page.category = newcategory
        current_page.divider_below = new_divider_below
        current_page.index = newindex
        db.session.commit()
        time.sleep(0.5)
        return redirect("/page/" + newname)

    return utils.render_with_navbar("editpage.html", form=form, title=title, index=index)


def delete_page(page_name):
    if not page_name:
        return utils.render_with_navbar("404.html"), 404

    page = Page.query.filter_by(name=page_name)
    if not page:
        return utils.render_with_navbar("404.html"), 404

    page.delete()
    db.session.commit()
    time.sleep(0.5)
    return redirect("/pages")

