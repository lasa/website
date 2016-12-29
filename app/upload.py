import os
from app import app, utils
from flask import Flask, redirect, request, url_for
from flask_wtf import Form
from wtforms import validators, FileField
from werkzeug.utils import secure_filename
import time


class UploadForm(Form):
    uploadfile = FileField('', [validators.DataRequired()])

def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        if form.uploadfile.name not in request.files:
            form.uploadfile.errors.append("Please select a valid file.")
            return utils.render_with_navbar("upload.html", form=form)

        f = request.files[form.uploadfile.name]
        filename = secure_filename(f.filename)
        f.save(os.path.join('app/', app.config['UPLOAD_FOLDER'], filename))
        f.close()
        time.sleep(0.5)
        #calls views.uploaded_file(filename)
        return redirect(url_for('uploaded_file', filename=filename))
        #TODO create a page at /uploads/ to view all uploads in a list and redirect to there instead

    return utils.render_with_navbar("upload.html", form=form)
