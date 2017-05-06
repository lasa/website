from app import db

# Define char limits allowed in names and passwords
USER_LIMITS = {'name': 16,
               'email': 50}

# Define char limits allowed in titles and bodies of posts
POST_LIMITS = {'title': 1000,
               'body': 30000}
# of pages
PAGE_LIMITS = {'title': 1000,
               'body': 75000}

# Define char limits allowed in fields for names, occupations, and emails
FACULTY_LIMITS = {'name': 50,
                  'occupation': 200,
                  'email': 50,
                  'tel': 30,
                  'website': 50}

LINK_LIMITS = {'title': 1000,
               'url': 200}

SLIDE_LIMITS = {'image_url': 200,
                'url': 200}


class User(db.Model):
    __tablename__ = "users"
    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(USER_LIMITS['name']), index=True, unique=True)
    email = db.Column('email', db.String(USER_LIMITS['email']), index=True, unique=True)
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
        return str(self.id_)

    def __repr__(self):
        return '<User %r>' % (self.name)


class Post(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(POST_LIMITS['title']))
    body = db.Column(db.Text())
    author = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Post %r>' % (self.title)

class Message(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(POST_LIMITS['title']))
    body = db.Column(db.Text())
    author = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Message %r>' % (self.title)

class Page(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(PAGE_LIMITS['title']))
    name = db.Column(db.String(PAGE_LIMITS['title']))
    category = db.Column(db.String(50))
    divider_below = db.Column(db.Boolean())
    index = db.Column(db.Integer)
    body = db.Column(db.Text())
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Page %r>' % (self.title)

class Link(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(LINK_LIMITS['title']))
    category = db.Column(db.String(50))
    divider_below = db.Column(db.Boolean())
    index = db.Column(db.Integer)
    url = db.Column(db.String(LINK_LIMITS['url']))

    def __repr__(self):
        return '<Link %r>' % (self.title)

class Slide(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(SLIDE_LIMITS['image_url']))
    url = db.Column(db.String(SLIDE_LIMITS['url']))

    def __repr__(self):
        return '<Slide %r>' % (self.id_)

class Faculty(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(FACULTY_LIMITS['name']))
    lastname = db.Column(db.String(FACULTY_LIMITS['name']))
    occupation = db.Column(db.String(FACULTY_LIMITS['occupation']))
    email = db.Column(db.String(FACULTY_LIMITS['email']))
    tel = db.Column(db.String(FACULTY_LIMITS['tel']))
    website = db.Column(db.String(FACULTY_LIMITS['website']))
    category = db.Column(db.String(50))

    def __repr__(self):
        return '<Faculty %r>' % (self.lastname)
