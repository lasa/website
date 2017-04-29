import time
import os

from app import app, utils
from flask import redirect, request
from flask_wtf import Form
from wtforms import validators, FileField
from werkzeug.utils import secure_filename


class UploadForm(Form):
    uploadfile = FileField('', [validators.DataRequired()])
    file_ = None
    filename = None

    def validate(self):
        if not Form.validate(self):
            return False
        if self.uploadfile.name not in request.files:
            self.uploadfile.errors.append("Please select a valid file.")
            return False

        self.file_ = request.files[self.uploadfile.name]
        self.filename = secure_filename(self.file_.filename)
        uploads = os.listdir(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']))

        if self.filename in uploads:
            self.uploadfile.errors.append("A file with this name already exists.")
            return False
        if not self.filename:
            self.uploadfile.errors.append("Invalid file name.")
            return False
        return True

def upload_file():
    form = UploadForm()
    if form.validate_on_submit():


        form.file_.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], form.filename))
        form.file_.close()
        time.sleep(0.5)
        return redirect('/uploads')

    return utils.render_with_navbar("upload/upload.html", form=form)

def show_uploads():
    uploads = os.listdir(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']))
    uploads.remove('.gitignore')
    # sorts uploads by time last modified, which should always be the same as time uploaded
    uploads.sort(key=lambda filename: os.stat(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)).st_mtime)
    return utils.render_with_navbar("upload/uploads.html", uploads=uploads[::-1])

def delete_upload():
    filename = request.args.get("name")
    if not filename:
        return redirect("/uploads")
    filename = secure_filename(filename)
    if not filename:
        return redirect("/uploads")

    try:
        os.remove(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
    except OSError:
        return redirect("/uploads")
    time.sleep(0.5)
    return redirect("/uploads")
