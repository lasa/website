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
        uploads = os.listdir(os.path.join('app', app.config['UPLOAD_FOLDER']))
        
        if filename in uploads:
            form.uploadfile.errors.append("A file with this name already exists.")
            return utils.render_with_navbar("upload.html", form=form)
        if not filename:
            form.uploadfile.errors.append("Invalid file name.")
            return utils.render_with_navbar("upload.html", form=form)

        f.save(os.path.join('app', app.config['UPLOAD_FOLDER'], filename))
        f.close()
        time.sleep(0.5)
        return redirect('/uploads')

    return utils.render_with_navbar("upload.html", form=form)

def show_uploads():
    uploads = os.listdir(os.path.join('app', app.config['UPLOAD_FOLDER']))
    uploads.remove('.gitignore')
    #sorts uploads by time last modified, which should always be the same as time uploaded
    uploads.sort(key=lambda filename:os.stat(os.path.join('app', app.config['UPLOAD_FOLDER'], filename)).st_mtime)
    return utils.render_with_navbar("uploads.html", uploads=uploads[::-1])

def delete_upload():
    filename = request.args.get("name")
    if not filename:
        return redirect("/uploads")
    filename = secure_filename(filename)
    if not filename:
        return redirect("/uploads")

    try:
        os.remove(os.path.join('app', app.config['UPLOAD_FOLDER'], filename))
    except FileNotFoundError:
        return redirect("/uploads")
    time.sleep(0.5)
    return redirect("/uploads")
