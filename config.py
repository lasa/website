import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = "lol"

SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/website'
SQLALCHEMY_TRACK_MODIFICATIONS = False
