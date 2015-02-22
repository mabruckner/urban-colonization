from flask import *

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment, Bundle

from htmlmin import minify
from flask.ext.login import LoginManager,login_user,logout_user, current_user, login_required
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from passlib.hash import pbkdf2_sha256

import os
import random


from Model import Model

app = Flask(__name__)
app.secret_key = "Secret"

login_manager = LoginManager()
login_manager.init_app(app)

model = Model(app)
db = model.db

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/uc.db'

app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

UPLOAD_FOLDER = '/tmp/uc-pics'

assets = Environment(app)
assets.url_expire = False

css = Bundle('css/main.css', 'css/bootstrap.css', filters="cssmin", output='css/gen/packed.css')
assets.register('css_all', css)

class LoginForm(Form):
    name = StringField('name',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])

class SignupForm(Form):
    name = StringField('name',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    repeatpassword = PasswordField('repeatpassword',validators=[DataRequired()])

def create_user(username,password):
    newuser = model.User(username,"")
    newuser.password = pbkdf2_sha256.encrypt(password)
    db.session.add(newuser)
    db.session.commit()

@login_manager.user_loader
def load_user(userid):
    users =  model.User.query.filter_by(username=userid)
    return users.first()

@app.route('/authenticate', methods=['GET','POST'])
def authenticate():
    form = LoginForm()
    if form.validate_on_submit():
        users = model.User.query.filter_by(username = request.form["name"])
        user = users.first()
        if user != None :
            if pbkdf2_sha256.verify(request.form["password"],user.password) :
                user.authenticated = True
                db.session.commit()
                login_user(user)
    return redirect(request.form["redirect"])

@app.route('/signin', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'GET' :
        return render_template("signin.html",form = form,error = "")
    error = "some fields were empty"
    if form.validate_on_submit():
        users = model.User.query.filter_by(username = request.form["name"])
        user = users.first()
        if user != None :
            if pbkdf2_sha256.verify(request.form["password"],user.password) :
                user.authenticated = True
                db.session.commit()
                login_user(user)
                return redirect("/")
        error = "incorrect username or password"
    return render_template("signin.html",form = form,error = error);

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()
    if request.method == 'GET' :
        return render_template("signup.html",form = form,error="")
    error = "some fields were empty"
    if form.validate_on_submit():
        error = "some fields were empty"
        if request.form["password"] == request.form["repeatpassword"] :
            newuser = model.User(request.form["name"],"")
            newuser.password = pbkdf2_sha256.encrypt(request.form["password"])
            newuser.authenticated = True
            db.session.add(newuser)
            db.session.commit()
            return redirect("/")
        else :
            error = "passwords did not match"
    return render_template("signup.html",form = form,error=error)

@login_required
@app.route('/signout')
def signout():
    logout_user()
    return redirect('/signin')

@login_required
@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(request.args.get("redirect"))

@login_required
@app.route('/makeuser', methods=['GET'])
def makeuser():
    admin = model.User('admin', 'admin@example.com')
    admin.password = pbkdf2_sha256.encrypt("password")
    db.session.add(admin)
    db.session.commit()
    return "True"

@login_required
@app.route('/makelichen', methods=['GET'])
def makelichen():
    l1 = model.Lichen("HELLO","img/lichen_wolf_eyes.jpg")
    l2 = model.Lichen("GOODBYE","img/lichen_wolf_eyes.jpg")
    db.session.add(l1)
    db.session.add(l2)
    db.session.commit()
    return "\\OoO/"

@login_required
@app.route('/getuser', methods=['GET'])
def getuser():
    admin = model.User.query.filter_by(username='admin').first()
    return admin.username

@login_required
@app.route('/', methods=['GET'])
def index():
    if current_user.is_anonymous():
        return redirect("/signin")
    return render_template('index.html',form=LoginForm(), hint=current_user.current_lichen.hint)

@login_required
@app.route('/lichens', methods=['GET','POST'])
def lichens():
    lichens = model.Lichen.query.all()
    return render_template('lichens.html',form=LoginForm(), lichens=lichens)

@login_required
@app.route('/lichens/<name>', methods=['GET','POST'])
def lichen(name):
    lichen = model.Lichen.query.filter_by(short_name=name).first()
    return render_template('lichen.html',form=LoginForm(), lichen=lichen)

@login_required
@app.route('/rotatelichen', methods=['GET','POST'])
def rotatelichen():
    lichen = model.User.get_random_lichen()
    current_user.current_lichen = lichen
    db.session.commit()
    return redirect("/")

@login_required
@app.route('/takepicture', methods=['GET'])
def takepicture():
    return render_template('takepicture.html')

@login_required
@app.route('/receivepicture', methods=['POST'])
def recievepicture():
    f = request.files['picture']
    if f:
        path = os.path.join(UPLOAD_FOLDER, f.filename)
        f.save(path)
        if True or current_user.current_lichen.verify(path):
            current_user.set_state(current_user.current_lichen, "found")
            current_user.current_lichen = random.choice(current_user.get_without_state())
            current_user.set_state(current_user.current_lichen, "looking")
            db.session.commit()
            return "YES!"
    return "Nooo"

@login_required
@app.route('/js/<remainder>',methods=['GET'])
@app.route('/img/<remainder>',methods=['GET'])
def get_static(remainder):
    return send_from_directory(app.static_folder,request.path[1:])

if __name__ == "__main__":
    app.run(host="0.0.0")
