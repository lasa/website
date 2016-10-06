from app import app, db
from app.models import User, Faculty
from flask import Flask, redirect, render_template, request
from flask_login import current_user
from flask_wtf import Form
from wtforms import validators, StringField, SelectField
from flask_wtf.html5 import TelField
from wtforms.validators import DataRequired

choices = [('admin', 'Administration'),
               ('teaching', 'Teaching'),
               ('guidance', 'Guidance and Counseling'),
               ('support', 'Support Staff'),
               ('other', 'Other')]
    
class NewFacultyForm(Form):
    firstname = StringField('First Name:', validators=[validators.DataRequired(), validators.Length(min=1,max=50)])
    lastname = StringField('Last Name:', validators=[validators.DataRequired(), validators.Length(min=1,max=50)])
    occupation = StringField('Position:', validators=[validators.DataRequired(), validators.Length(min=1,max=200)])
    email = StringField('Email:', validators=[validators.DataRequired(), validators.email(), validators.Length(min=1,max=50)])

    telregex = r'^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$'
    tel = TelField('Telephone Number (optional):', validators=[validators.Optional(), validators.Regexp(telregex, message="Must be a valid telephone number.")])

    websiteregex = r'(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
    website = StringField('Website (optional):', validators=[validators.Optional(), validators.Regexp(websiteregex, message="Must be a valid URL."), validators.Length(min=0,max=50)])

    category = SelectField('Category:', choices=choices)


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

        newfaculty = Faculty(firstname=firstname, lastname=lastname, occupation=occupation, email=email, tel=tel, website=website,  category=category)
        db.session.add(newfaculty)
        db.session.commit()
        return redirect("/faculty")

    return render_template("faculty/newfaculty.html", form=form)

def edit_faculty():
    facultyid = request.args.get("id")
    if not facultyid: 
        return redirect("/newfaculty")

    currentFaculty = Faculty.query.filter_by(id=facultyid).first()
    if not currentFaculty:
        return redirect("/newfaculty")

    firstname = currentFaculty.firstname
    lastname = currentFaculty.lastname
    occupation = currentFaculty.occupation
    email = currentFaculty.email
    tel = currentFaculty.tel
    website = currentFaculty.website
    category = currentFaculty.category

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

        currentFaculty.firstname = newfirstname
        currentFaculty.lastname = newlastname
        currentFaculty.occupation = newoccupation
        currentFaculty.email = newemail
        currentFaculty.tel = newtel
        currentFaculty.website = newwebsite
        currentFaculty.category = newcategory

        db.session.commit()
        return redirect("/faculty")

    if not website:
        website = ""
    return render_template("faculty/editfaculty.html", form=form, firstname=firstname, lastname=lastname, occupation=occupation, email=email, tel=tel, website=website)

def delete_faculty():
    facultyid = request.args.get("id")
    if not facultyid:
        return redirect("/faculty")

    faculty = Faculty.query.filter_by(id=facultyid)
    faculty.delete()
    db.session.commit()
    return redirect("/faculty")
