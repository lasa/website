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
    index = IntegerField('Ordering index (lower number = higher up in dropdown menu):', validators=[validators.Optional()])  # not actually optional
    body = TextAreaField('Body:', validators=[validators.Length(min=0, max=75000)], widget=utils.TinyMCE)
    bodyhtml = HiddenField()



def new_page():
    form = NewPageForm()
    if form.validate_on_submit():
        data = {"title": form.title.data,
                "body": form.bodyhtml.data,
                "category": form.category.data,
                "divider_below": form.divider_below.data,
                "index": form.index.data}

        # do manual validation because form.body.data needs to be set after
        # a failed validation and WTForm's validation system does not
        # allow for a post-failed-validation hook

        if len(data["title"]) < 1:
            form.title.errors.append("This field is required.")

        if not data["index"] or (data["index"] < 0 or data["index"] > 100):
            form.index.errors.append("Must be a number between 0 and 100.")

        data["name"] = "-".join(data["title"].split(" ")).lower()

        if Page.query.filter_by(name=data["name"]).first():
            form.title.errors.append("A page with this name already exists.")

        # if there are any errors, return the form again with form.body.data preserved
        for key in data.keys():
            try:
                if len(getattr(form, key).errors) > 0:
                    form.body.data = data["body"]
                    return utils.render_with_navbar("newpage.html", form=form, **data)
            except AttributeError:
                pass

        newpage = Page(**data)
        db.session.add(newpage)
        db.session.commit()
        time.sleep(0.5)
        return redirect("/page/" + data["name"])

    return utils.render_with_navbar("newpage.html", form=form)


def edit_page(page_name):
    if not page_name:
        return utils.render_with_navbar("404.html"), 404

    current_page = Page.query.filter_by(name=page_name).first()
    if not current_page:
        return utils.render_with_navbar("404.html"), 404

    data = {"title": current_page.title,
            "body": current_page.body,
            "category": current_page.category,
            "divider_below": current_page.divider_below,
            "index": current_page.index}

    form = NewPageForm(**data)

    if form.validate_on_submit():
        new_data = {"title": form.title.data,
                    "body": form.bodyhtml.data,
                    "category": form.category.data,
                    "divider_below": form.divider_below.data,
                    "index": form.index.data}

        # do manual validation because form.body.data needs to be set after
        # a failed validation and WTForm's validation system does not
        # allow for a post-failed-validation hook

        if len(new_data["title"]) < 1:
            form.title.errors.append("This field is required.")

        if not new_data["index"] or (new_data["index"] < 0 or new_data["index"] > 100):
            form.index.errors.append("Must be a number between 0 and 100.")

        new_data["name"] = "-".join(new_data["title"].split(" ")).lower()

        if new_data["name"] != page_name and Page.query.filter_by(name=new_data["name"]).first():
            form.title.errors.append("A page with this name already exists.")

        # if there are any errors, return the form again with form.body.data preserved
        for key in new_data.keys():
            try:
                if len(getattr(form, key).errors) > 0:
                    form.body.data = new_data["body"]
                    return utils.render_with_navbar("newpage.html", form=form, **new_data)
            except AttributeError:
                pass

        for key, value in new_data.items():
            setattr(current_page, key, value)
        db.session.commit()
        time.sleep(0.5)
        return redirect("/page/" + new_data["name"])

    return utils.render_with_navbar("editpage.html", form=form, **data)


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

