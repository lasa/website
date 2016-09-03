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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(user_limits['name']), index=True, unique=True)
    email = db.Column(db.String(user_limits['email']), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(post_limits['title']))
    body = db.Column(db.String(post_limits['body']))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(post_limits['title']))
    body = db.Column(db.String(post_limits['body']))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Page %r>' % (self.body)
