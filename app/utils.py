from app import app
from app.models import Page
from flask import render_template

def render_with_navbar(template, **kwargs):
    pages = {'calendars': Page.query.filter_by(category='calendars').order_by(Page.index.asc()),
                'about': Page.query.filter_by(category='about').order_by(Page.index.asc()),
                'academics': Page.query.filter_by(category='academics').order_by(Page.index.asc()),
                'students': Page.query.filter_by(category='students').order_by(Page.index.asc()),
                'parents': Page.query.filter_by(category='parents').order_by(Page.index.asc()),
                'admissions': Page.query.filter_by(category='admissions').order_by(Page.index.asc())}
    return render_template(template, pages=pages, **kwargs)


