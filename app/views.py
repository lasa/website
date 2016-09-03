from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
@app.route('/history')
def history():
	return render_template("history.html")