#!flask/bin/python
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path

engine = create_engine(SQLALCHEMY_DATABASE_URI[0:SQLALCHEMY_DATABASE_URI.rfind('/')])
engine.execute("CREATE DATABASE " + SQLALCHEMY_DATABASE_URI.split('/')[-1] + ';')
engine.execute("USE " + SQLALCHEMY_DATABASE_URI.split('/')[-1] + ';')
db.create_all()
