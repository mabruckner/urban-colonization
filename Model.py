from flask.ext.sqlalchemy import SQLAlchemy

class Model():
    def __init__(self, app):
        self.db = SQLAlchemy(app)
        db = self.db

        class User(self.db.Model):
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(80), unique=True)
            email = db.Column(db.String(120), unique=True)
            password = db.Column(db.String)
            authenticated = db.Column(db.Boolean())

            def __init__(self, username, email):
                self.username = username
                self.email = email
                self.authenticated = False

            def __repr__(self):
                return '<User %r>' % self.username

            def is_authenticated(self) :
                print(self.email)
                return self.authenticated

            def is_active(self) :
                return self.is_authenticated()

            def is_anonymous(self) :
                return False

            def get_id(self) :
                return self.email

        self.User = User

        class Lichen(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String)
            image = db.Column(db.String)
            description = db.Column(db.String)
            def __init__(self, name, imagepath):
                self.image = imagepath
                self.name = name

        self.Lichen = Lichen
