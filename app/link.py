import time

from app import db, utils
from app.models import Link
from flask import redirect, request
from flask_wtf import Form
from flask_wtf.html5 import IntegerField
from wtforms import validators, StringField, SelectField, BooleanField

CHOICES = [('Calendars', 'Calendars'),
           ('About Us', 'About Us'),
           ('Academics', 'Academics'),
           ('Students', 'Students'),
           ('Parents', 'Parents'),
           ('Admissions', 'Admissions')]

URL_REGEX = r'((http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&/=]*))|\/[-a-zA-Z0-9@:%_\+.~#?&/=]*'

class NewLinkForm(Form):
    title = StringField('Title:', validators=[validators.InputRequired(), validators.Length(min=0, max=1000)])
    category = SelectField('Category:', choices=CHOICES)
    divider_below = BooleanField('Divider below link in dropdown menu')
    index = IntegerField('Ordering index:', validators=[validators.Optional()])  # not actually optional

    link_list = SelectField('Choose from uploads: ')
    url = StringField('URL (external link or relative path): ', validators=[validators.InputRequired(), validators.Regexp(URL_REGEX, message="Invalid URL. Must be a valid external link or a relative URL beginning with '/'."), validators.Length(min=0, max=200)])

    def __init__(self, **kwargs):
        Form.__init__(self, **kwargs)
        self.link_list.choices = utils.get_uploads()[1] # gets non-images only

    def validate(self):
        is_valid = True
        is_valid = Form.validate(self)
        if not (self.url.data.startswith('/') or self.url.data.startswith("http://") or self.url.data.startswith("https://")):
            self.url.data = "http://" + self.url.data

        if self.index.data is not None and (self.index.data < 0 or self.index.data > 100):
            self.index.errors.append("Must be a number between 0 and 100.")
            is_valid = False
        elif self.index.data is None:
            self.index.data = 101

        return is_valid


def new_link():
    form = NewLinkForm()
    if form.validate_on_submit():
        data = {"title": form.title.data,
                "category": form.category.data,
                "divider_below": form.divider_below.data,
                "index": form.index.data,
                "url": form.url.data}

        newlink = Link(**data)
        db.session.add(newlink)
        db.session.commit()
        time.sleep(0.5)
        return redirect("/pages")

    return utils.render_with_navbar("link/form.html", form=form)

def edit_link():
    linkid = request.args.get("id")
    if not linkid:
        return redirect("/newlink")

    current_link = Link.query.filter_by(id_=linkid).first()
    if not current_link:
        return redirect("/newlink")

    data = {"title": current_link.title,
            "category": current_link.category,
            "divider_below": current_link.divider_below,
            "index": None if current_link.index == 101 else current_link.index,
            "url": current_link.url}

    form = NewLinkForm(**data)

    if form.validate_on_submit():
        new_data = {"title": form.title.data,
                    "category": form.category.data,
                    "divider_below": form.divider_below.data,
                    "index": form.index.data,
                    "url": form.url.data}

        for key, value in new_data.items():
            setattr(current_link, key, value)
        db.session.commit()
        time.sleep(0.5)
        return redirect("/pages")

    return utils.render_with_navbar("link/form.html", form=form)

def delete_link():
    linkid = request.args.get("id")
    if not linkid:
        return redirect("/pages")

    link = Link.query.filter_by(id_=linkid)
    link.delete()
    db.session.commit()
    time.sleep(0.5)
    return redirect("/pages")
