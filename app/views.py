from app import app, login_signup, models, login_manager, post, faculty
from app.models import User, Post, Faculty
from flask_login import login_required
from flask import render_template, request

@app.route('/')
@app.route('/index/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template("index.html", posts=posts)

@app.route('/news/')
def news():
    if request.args.get("postid"):
        post = Post.query.filter_by(id=request.args.get("postid")).first()
        if post:
            return render_template("newsitem.html", post=post)
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template("news.html", posts=posts)

@app.route('/faculty/')
def all_faculty():
    faculty = Faculty.query.order_by(Faculty.lastname.asc())
    return render_template("faculty.html", faculty=faculty, title="Faculty")

@app.route('/administration/')
def administration():
    administrators = Faculty.query.filter_by(category="administrators").order_by(Faculty.lastname.asc())
    return render_template("faculty.html", faculty=administrators, title="Administration")

@app.route('/guidance/')
def guidance():
    counselors = Faculty.query.filter_by(category="guidance").order_by(Faculty.lastname.asc())
    return render_template("faculty.html", faculty=counselors, title="Guidance and Counseling")

@app.route('/teachers/')
def teachers():
    teachers = Faculty.query.filter_by(category="teaching").order_by(Faculty.lastname.asc())
    return render_template("faculty.html", faculty=teachers, title="Teachers")

@app.route('/support/')
def support():
    support = Faculty.query.filter_by(category="support").order_by(Faculty.lastname.asc())
    return render_template("faculty.html", faculty=support, title="Support Staff")


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

@app.route('/probation/')
def probation():
    return render_template("probation.html")

@app.route('/schedule/')
def schedule():
    return render_template("schedule.html")

@app.route('/calendar/')
def calendar():
    return render_template("calendar.html")

@app.route('/calendar/college/')
def calendar_college():
    return render_template("calendar/college.html")

@app.route('/calendar/athletic/')
def calendar_athletic():
    return render_template("calendar/athletic.html")

@app.route('/college/')
def college():
    return render_template("college.html")

@app.route('/college/sessions/')
def college_sessions():
    return render_template("college/sessions.html")

@app.route('/college/reps/')
def college_reps():
    return render_template("college/reps.html")

@app.route('/college/testing/')
def college_testing():
    return render_template("college/testing.html")

@app.route('/college/faq/')
def college_faq():
    return render_template("college/faq.html")

@app.route('/college/aid/')
def college_aid():
    return render_template("college/aid.html")

@app.route('/college/naviance/')
def college_naviance():
    return render_template("college/naviance.html")

@app.route('/courseguide/')
def course_guide():
    return render_template("courseguide.html")

@app.route('/coursefaq/')
def course_faq():
    return render_template("coursefaq.html")

@app.route('/honorcode/')
def honor_code():
    return render_template("honorcode.html")

@app.route('/magnetendorsement')
def magnet_endorsement():
    return render_template("magnetendorsement.html")

@app.route('/finearts')
def fine_arts():
    return render_template("finearts.html")

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

@app.route("/editpost/", methods=["GET", "POST"])
@login_required
def edit_post():
    return post.edit_post()

@app.route("/delpost/")
@login_required
def delete_post():
    return post.delete_post()

@app.route("/newfaculty/", methods=["GET", "POST"])
@login_required
def new_faculty():
    return faculty.new_faculty()

@app.route("/editfaculty/", methods=["GET", "POST"])
@login_required
def edit_faculty():
    return faculty.edit_faculty()

@app.route("/delfaculty/")
@login_required
def delete_faculty():
    return faculty.delete_faculty()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
