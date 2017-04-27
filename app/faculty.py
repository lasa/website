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

TEL_REGEX = r'^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$'

URL_REGEX = r'(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'

class NewFacultyForm(Form):
    firstname = StringField('First Name:', validators=[validators.DataRequired(), validators.Length(min=1, max=50)])
    lastname = StringField('Last Name:', validators=[validators.DataRequired(), validators.Length(min=1, max=50)])
    occupation = StringField('Position:', validators=[validators.DataRequired(), validators.Length(min=1, max=200)])
    email = StringField('Email:', validators=[validators.DataRequired(), validators.email(), validators.Length(min=1, max=50)])

    tel = TelField('Telephone Number (optional):', validators=[validators.Optional(), validators.Regexp(TEL_REGEX, message="Must be a valid telephone number.")])

    website = StringField('Website (optional):', validators=[validators.Optional(), validators.Regexp(URL_REGEX, message="Must be a valid URL."), validators.Length(min=0, max=50)])

    category = SelectField('Category:', choices=CHOICES)


def new_faculty():
    form = NewFacultyForm()
    if form.validate_on_submit():
        data = {"firstname": form.firstname.data,
                "lastname": form.lastname.data,
                "occupation": form.occupation.data,
                "email": form.email.data,
                "tel": form.tel.data,
                "website": form.website.data,
                "category": form.category.data}

        if data["website"].isspace():
            data["website"] = None
        if data["website"] and not (data["website"].startswith("http://") or data["website"].startswith("https://")):
            data["website"] = "http://" + data["website"]


        newfaculty = Faculty(**data)
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

    data = {"firstname": current_faculty.firstname,
            "lastname": current_faculty.lastname,
            "occupation": current_faculty.occupation,
            "email": current_faculty.email,
            "tel": current_faculty.tel,
            "website": current_faculty.website,
            "category": current_faculty.category}

    form = NewFacultyForm(**data)

    if form.validate_on_submit():
        new_data = {"firstname": form.firstname.data,
                    "lastname": form.lastname.data,
                    "occupation": form.occupation.data,
                    "email": form.email.data,
                    "tel": form.tel.data,
                    "website": form.website.data,
                    "category": form.category.data}

        if new_data["website"].isspace():
            new_data["website"] = None
        if new_data["website"] and not (new_data["website"].startswith("http://") or new_data["website"].startswith("https://")):
            new_data["website"] = "http://" + new_data["website"]

        for key, value in new_data.items():
            setattr(current_faculty, key, value)
        db.session.commit()
        time.sleep(0.5)
        return redirect("/faculty")

    return utils.render_with_navbar("faculty/editfaculty.html", form=form)

def delete_faculty():
    facultyid = request.args.get("id")
    if not facultyid:
        return redirect("/faculty")

    faculty = Faculty.query.filter_by(id_=facultyid)
    faculty.delete()
    db.session.commit()
    time.sleep(0.5)
    return redirect("/faculty")
