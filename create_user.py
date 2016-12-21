#!flask/bin/python

from app import db, models
from sys import argv
import bcrypt

u = models.User(name=argv[1], email=argv[2], password=bcrypt.hashpw(argv[3].encode("utf-8"), bcrypt.gensalt()))
db.session.add(u)
db.session.commit()
