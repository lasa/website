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
    name = None

    def __init__(self, name=None, **kwargs):
        Form.__init__(self, **kwargs)
        self.name = name

    def validate(self):
        is_valid = True
        is_valid = Form.validate(self)

        # do manual validation
        if len(self.title.data) < 1:
            self.title.errors.append("This field is required.")
            is_valid = False

        if not self.index.data or (self.index.data < 0 or self.index.data > 100):
            self.index.errors.append("Must be a number between 0 and 100.")
            is_valid = False

        old_name = self.name
        print(old_name)
        self.name = "-".join(self.title.data.split(" ")).lower()

        if self.name != old_name and Page.query.filter_by(name=self.name).first():
            self.title.errors.append("A page with this name already exists.")
            is_valid = False

        self.body.data = self.bodyhtml.data  # preserve what has already been entered
        return is_valid



def new_page():
    form = NewPageForm()

    if form.validate_on_submit():
        data = {"title": form.title.data,
                "body": form.bodyhtml.data,
                "category": form.category.data,
                "divider_below": form.divider_below.data,
                "index": form.index.data,
                "name": form.name}

        newpage = Page(**data)
        db.session.add(newpage)
        db.session.commit()
        time.sleep(0.5)
        return redirect("/page/" + form.name)

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
            "index": current_page.index,
            "name": page_name}

    form = NewPageForm(**data)

    if form.validate_on_submit():
        new_data = {"title": form.title.data,
                    "body": form.bodyhtml.data,
                    "category": form.category.data,
                    "divider_below": form.divider_below.data,
                    "index": form.index.data,
                    "name": form.name}

        for key, value in new_data.items():
            setattr(current_page, key, value)
        db.session.commit()
        time.sleep(0.5)
        return redirect("/page/" + new_data["name"])

    return utils.render_with_navbar("editpage.html", form=form)


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
