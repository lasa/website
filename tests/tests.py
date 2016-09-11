#!../flask/bin/python
import os
import unittest
import bcrypt
import hmac

from config import basedir
from app import app, db
from app.models import User


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_signup(self):
        u = User(name="harambe", email="harambe@cincinnatizoo.org",
                 password=bcrypt.hashpw("IAmHarambe".encode("utf-8"), bcrypt.gensalt2()))
        db.session.add(u)
        db.session.commit()

if __name__ == '__main__':
    unittest.main()
