import time

from app import db, utils
from app.models import Faculty
from flask import redirect, request
from flask_wtf import Form
from flask_wtf.html5 import TelField
from wtforms import validators, StringField, SelectField

CHOICES = [('admin', 'Administration'),
           ('teaching', 'Teaching'),
           ('guidance', 'Guidance and Counseling'),
           ('support', 'Support Staff'),
           ('other', 'Other')]

class NewFacultyForm(Form):
    firstname = StringField('First Name:', validators=[validators.DataRequired(), validators.Length(min=1, max=50)])
    lastname = StringField('Last Name:', validators=[validators.DataRequired(), validators.Length(min=1, max=50)])
    occupation = StringField('Position:', validators=[validators.DataRequired(), validators.Length(min=1, max=200)])
    email = StringField('Email:', validators=[validators.DataRequired(), validators.email(), validators.Length(min=1, max=50)])

    telregex = r'^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$'
    tel = TelField('Telephone Number (optional):', validators=[validators.Optional(), validators.Regexp(telregex, message="Must be a valid telephone number.")])

    websiteregex = r'(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
    website = StringField('Website (optional):', validators=[validators.Optional(), validators.Regexp(websiteregex, message="Must be a valid URL."), validators.Length(min=0, max=50)])

    category = SelectField('Category:', choices=CHOICES)


def new_faculty():
    form = NewFacultyForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        occupation = form.occupation.data
        email = form.email.data
        tel = form.tel.data
        website = form.website.data
        if website.isspace():
            website = None
        if website and not (website.startswith("http://") or website.startswith("https://")):
            website = "http://" + website

        category = form.category.data

        newfaculty = Faculty(firstname=firstname, lastname=lastname, occupation=occupation, email=email, tel=tel, website=website, category=category)
        db.session.add(newfaculty)
        db.session.commit()
        time.sleep(0.5)
        return redirect("/faculty")

    return utils.render_with_navbar("faculty/newfaculty.html", form=form)

def edit_faculty():
    facultyid = request.args.get("id")
    if not facultyid:
        return redirect("/newfaculty")

    current_faculty = Faculty.query.filter_by(id_=facultyid).first()
    if not current_faculty:
        return redirect("/newfaculty")

    firstname = current_faculty.firstname
    lastname = current_faculty.lastname
    occupation = current_faculty.occupation
    email = current_faculty.email
    tel = current_faculty.tel
    website = current_faculty.website
    category = current_faculty.category

    form = NewFacultyForm(category=category)

    if form.validate_on_submit():
        newfirstname = form.firstname.data
        newlastname = form.lastname.data
        newoccupation = form.occupation.data
        newemail = form.email.data
        newtel = form.tel.data
        newwebsite = form.website.data
        if newwebsite.isspace():
            newwebsite = None
        if newwebsite and not (newwebsite.startswith("http://") or newwebsite.startswith("https://")):
            newwebsite = "http://" + newwebsite

        newcategory = form.category.data

        current_faculty.firstname = newfirstname
        current_faculty.lastname = newlastname
        current_faculty.occupation = newoccupation
        current_faculty.email = newemail
        current_faculty.tel = newtel
        current_faculty.website = newwebsite
        current_faculty.category = newcategory

        db.session.commit()
        time.sleep(0.5)
        return redirect("/faculty")

    if not website:
        website = ""
    return utils.render_with_navbar("faculty/editfaculty.html", form=form, firstname=firstname, lastname=lastname, occupation=occupation, email=email, tel=tel, website=website)

def delete_faculty():
    facultyid = request.args.get("id")
    if not facultyid:
        return redirect("/faculty")

    faculty = Faculty.query.filter_by(id_=facultyid)
    faculty.delete()
    db.session.commit()
    time.sleep(0.5)
    return redirect("/faculty")
