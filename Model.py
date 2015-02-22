from flask.ext.sqlalchemy import SQLAlchemy
import random
from perform import zbarimg
import json

class Model():
    def __init__(self, app):
        self.db = SQLAlchemy(app)
        db = self.db

        class Lichen(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            short_name = db.Column(db.String)
            name = db.Column(db.String)
            image = db.Column(db.String)
            description = db.Column(db.String)
            passcode = db.Column(db.String)
            hint = db.Column(db.String)
            num_found = db.Column(db.Integer)

            def __init__(self, short_name, name, imagepath):
                self.image = imagepath
                self.name = name
                self.short_name = short_name
                self.num_found = 0

            def verify(self,filepath):
                contents = zbarimg(filepath)
                return self.passcode in contents

            def __str__(self):
                return "(({}, {}, {}, {}))".format(self.id, self.name, self.image, self.description)

        self.Lichen = Lichen

        class User(self.db.Model):
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(80), unique=True)
            email = db.Column(db.String(120), unique=True)
            password = db.Column(db.String)
            authenticated = db.Column(db.Boolean())
            is_first_time = db.Column(db.Boolean())
            hint_access = db.Column(db.String)

            current_lichen_id = db.Column(db.Integer, db.ForeignKey('lichen.id'))
            current_lichen = db.relationship('Lichen', backref=db.backref('users', lazy='dynamic'))

            def __init__(self, username, email):
                self.username = username
                self.email = email
                self.authenticated = False
                self.is_first_time = True
                self.current_lichen = User.get_random_lichen()
                clue_map = {str(self.current_lichen.id) : "looking" }
                self.hint_access = json.dumps(clue_map)

            def __repr__(self):
                return '<User %r>' % self.username

            def is_authenticated(self) :
                return self.authenticated

            def is_active(self) :
                return self.is_authenticated()

            def is_anonymous(self) :
                return False

            def get_id(self) :
                return self.username

            def get_state_for(self,clueval):
                cluemap = json.loads(self.hint_access)
                return cluemap[clueval]

            def get_with_state(self,state):
                cluemap = json.loads(self.hint_access)
                cluestrings = []
                for cluestring in cluemap :
                    if cluemap[cluestring] == state :
                        cluestrings.append(cluestring)
                q = Lichen.query.all()
                output = []
                for lichen in q :
                    if str(lichen.id) in cluestrings :
                        output.append(lichen)
                return output

            def get_without_state(self):
                cluemap = json.loads(self.hint_access)
                cluestrings = []
                for cluestring in cluemap:
                    if cluemap[cluestring] != "" :
                        cluestrings.append(cluestring)
                q = Lichen.query.all()
                output = []
                for lichen in q :
                    if str(lichen.id) not in cluestrings :
                        output.append(lichen)
                return output

            def get_looking(self):
                return self.get_with_state("looking")

            def get_found(self):
                return self.get_with_state("found")

            def set_state(self,lichen,state):
                l_map = json.loads(self.hint_access)
                l_map[str(lichen.id)] = state
                self.hint_access = json.dumps(l_map)
                db.session.commit()

            @staticmethod
            def get_random_lichen():
                lichens = Lichen.query.all()
                if len(lichens) > 0:
                    return random.choice(lichens)
                else:
                    return None #TODO: handle this later

        self.User = User
