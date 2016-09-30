from app import db

# Define char limits allowed in names and passwords
user_limits = {'name': 16,
               'email': 50}

# Define char limits allowed in titles and bodies of posts
post_limits = {'title': 1000,
               'body': 30000}
# of pages
page_limits = {'title': 1000,
               'body': 75000}

# Define char limits allowed in fields for names, occupations, and emails
faculty_limits = {'name': 50,
                  'occupation': 200,
                  'email': 50,
                  'tel': 30,
                  'website': 50}


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(user_limits['name']), index=True, unique=True)
    email = db.Column('email', db.String(user_limits['email']), index=True, unique=True)
    password = db.Column('password', db.String(255))

    def __init__(self, name, password, email):
        self.name = name
        self.email = email
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(post_limits['title']))
    body = db.Column(db.Text())
    author = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Post %r>' % (self.title)


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(post_limits['title']))
    body = db.Column(db.Text())
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Page %r>' % (self.title)

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(faculty_limits['name']))
    lastname = db.Column(db.String(faculty_limits['name']))
    occupation = db.Column(db.String(faculty_limits['occupation']))
    email = db.Column(db.String(faculty_limits['email']))
    tel = db.Column(db.String(faculty_limits['tel']))
    website = db.Column(db.String(faculty_limits['website']))
    category = db.Column(db.String(50))

    def __repr__(self):
        return '<Faculty %r>' % (self.lastname)
