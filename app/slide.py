import os
import time

from app import app, db, utils
from app.models import Post, Slide
from flask import redirect, request
from flask_wtf import Form
from wtforms import validators, StringField, SelectField

URL_REGEX = r'((http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&/=]*))|\/[-a-zA-Z0-9@:%_\+.~#?&/=]*'

def generate_lists():
    images = [('none', '')]
    links = [('none', '')]
    news = [('none', '')]

    uploads = os.listdir(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']))
    uploads.remove(".gitignore")
    image_extensions = ["png", "jpg", "jpeg", "gif", "bmp"]

    for upload in uploads:
        if '.' in upload and upload.rsplit('.', 1)[1].lower() in image_extensions:
            images.append(('/uploads/' + upload, upload))
        else:
            links.append(('/uploads/' + upload, upload))

    posts = Post.query.order_by(Post.timestamp.desc()).limit(10)
    for post in posts:
        news.append(('/news?postid=' + str(post.id_), post.title if len(post.title) <= 30 else post.title[:30] + "..."))

    return images, links, news


class NewSlideForm(Form):
    images, links, news = generate_lists()

    image_list = SelectField('Choose from uploads: ', choices=images)
    image_url = StringField('URL (external link or relative path): ', validators=[validators.InputRequired(), validators.Regexp(URL_REGEX, message="Invalid URL. Must be a valid external link or a relative URL beginning with '/'."), validators.Length(min=0, max=200)])

    link_list = SelectField('Choose from uploads: ', choices=links)
    news_list = SelectField('Choose from news: ', choices=news)
    url = StringField('URL (external link or relative path): ', validators=[validators.InputRequired(), validators.Regexp(URL_REGEX, message="Invalid URL. Must be a valid external link or a relative URL beginning with '/'."), validators.Length(min=0, max=200)])

    def validate(self):
        is_valid = True
        is_valid = Form.validate(self)

        if not (self.image_url.data.startswith('/') or self.image_url.data.startswith("http://") or self.image_url.data.startswith("https://")):
            self.image_url.data = "http://" + self.image_url.data

        if not (self.url.data.startswith('/') or self.url.data.startswith("http://") or self.url.data.startswith("https://")):
            self.url.data = "http://" + self.url.data

        return is_valid


def new_slide():
    form = NewSlideForm()
    if form.validate_on_submit():
        data = {"image_url": form.image_url.data,
                "url": form.url.data}

        newslide = Slide(**data)
        db.session.add(newslide)
        db.session.commit()
        time.sleep(0.5)
        return redirect("/slides")

    return utils.render_with_navbar("slide/form.html", form=form)

def edit_slide():
    id_ = request.args.get("id")
    if not id_:
        return redirect("/newslide")

    current_slide = Slide.query.filter_by(id_=id_).first()
    if not current_slide:
        return redirect("/newslide")

    data = {"image_url": current_slide.image_url,
            "url": current_slide.url}

    form = NewSlideForm(**data)

    if form.validate_on_submit():
        new_data = {"image_url": form.image_url.data,
                    "url": form.url.data}

        for key, value in new_data.items():
            setattr(current_slide, key, value)
        db.session.commit()
        time.sleep(0.5)
        return redirect("/slides")

    return utils.render_with_navbar("slide/form.html", form=form)

def delete_slide():
    id_ = request.args.get("id")
    if not id_:
        return redirect("/slides")

    slide = Slide.query.filter_by(id_=id_)
    slide.delete()
    db.session.commit()
    time.sleep(0.5)
    return redirect("/slides")
