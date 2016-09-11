from app import app, login_signup, models, login_manager, post
from app.models import User, Post
from flask_login import login_required
from flask import render_template, request

@app.route('/')
@app.route('/index/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template("index.html", posts=posts)

@app.route('/news')
def news():
    if request.args.get("postid"):
        post = Post.query.filter_by(id=request.args.get("postid")).first()
        if post:
            return render_template("newsitem.html", post=post)
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template("news.html", posts=posts)


@app.route('/history/')
def history():
    return render_template("history.html")

@app.route('/profile/')
def profile():
    return render_template("profile.html")

@app.route('/accolades/')
def accolades():
    return render_template("accolades.html")

@app.route('/contact/')
def contact():
    return render_template("contact.html")

@app.route('/mission/')
@app.route('/vision/')
def mission():
    return render_template("mission.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    return login_signup.login()

@app.route("/logout/", methods=["GET", "POST"])
def logout():
    return login_signup.logout()

@app.route("/newpost/", methods=["GET", "POST"])
@login_required
def new_post():
    return post.new_post()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
