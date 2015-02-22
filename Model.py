from flask.ext.sqlalchemy import SQLAlchemy
import random

class Model():
    def __init__(self, app):
        self.db = SQLAlchemy(app)
        db = self.db

        class Lichen(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String)
            image = db.Column(db.String)
            description = db.Column(db.String)
            def __init__(self, name, imagepath):
                self.image = imagepath
                self.name = name

            def __str__(self):
                return "(({}, {}, {}, {}))".format(self.id, self.name, self.image, self.description)

        self.Lichen = Lichen

        class Clue(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            text = db.Column(db.String)
            target = db.Column(db.Integer)
            def __init__(self, text, target):
                self.text = text
                self.target = target

            def __str__(self):
                return "(({}, {}, {}))".format(self.id, self.text, self.target)

        class User(self.db.Model):
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(80), unique=True)
            email = db.Column(db.String(120), unique=True)
            password = db.Column(db.String)
            authenticated = db.Column(db.Boolean())
            is_first_time = db.Column(db.Boolean())
            hint_access = db.Column(db.String)

            current_clue_id = db.Column(db.Integer, db.ForeignKey('clue.id'))
            current_clue = db.relationship('Clue', backref=db.backref('users', lazy='dynamic'))

            def __init__(self, username, email):
                self.username = username
                self.email = email
                self.authenticated = False
                self.is_first_time = True
                self.current_clue = self.get_initial_clue()
                self.hint_access = "{}"

            def __repr__(self):
                return '<User %r>' % self.username

            def is_authenticated(self) :
                return self.authenticated

            def is_active(self) :
                return self.is_authenticated()

            def is_anonymous(self) :
                return False

            def get_id(self) :
                return self.email

            def get_initial_clue(self):
                clues = Clue.query.all()
                if len(clues) > 0:
                    return random.choice(clues)
                else:
                    return None #TODO: handle this later

        self.User = User

        self.Clue = Clue
