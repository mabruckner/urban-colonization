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
    email = StringField('email',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    repeatpassword = PasswordField('repeatpassword',validators=[DataRequired()])

def create_user(username,email,password):
    newuser = model.User(username,email)
    newuser.password = pbkdf2_sha256.encrypt(password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

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
            user = create_user(request.form["name"],request.form["email"],request.form["password"])
            user.authenticated = True
            db.session.commit()
            login_user(user)
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
    return render_template('index.html',form=LoginForm(), hint=current_user.current_lichen.hint, alert=request.args.get('alert', ""), alert_type=request.args.get('alert_type', ''))

@login_required
@app.route('/lichens', methods=['GET','POST'])
def lichens():
    looking = current_user.get_looking()
    found = current_user.get_found()
    locked = current_user.get_without_state()
    return render_template('lichens.html',form=LoginForm(), looking = looking, found = found,locked = locked)

@login_required
@app.route('/lichens/<name>', methods=['GET','POST'])
def lichen(name):
    lichen = model.Lichen.query.filter_by(short_name=name).first()
    locked = lichen in current_user.get_without_state()
    unfound = lichen not in current_user.get_found()
    return render_template('lichen.html',form=LoginForm(), lichen=lichen,locked = locked,unfound = unfound)

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
        if current_user.current_lichen.verify(path):
            current_user.set_state(current_user.current_lichen, "found")
            current_user.current_lichen.num_found +=1

            name = current_user.current_lichen.name
            num = current_user.current_lichen.num_found

            lichens_left = current_user.get_without_state()
            if len(lichens_left) > 0:
                current_user.current_lichen = random.choice(lichens_left)
                current_user.set_state(current_user.current_lichen, "looking")
                db.session.commit()
                return redirect("/?alert_type=success&alert=Found {}! - You are finder number {}".format(name, num))
            else:
                db.session.commit()
                return redirect("/?alert_type=success&alert=Found {}! - You are finder number {} - Congratz, you found all lichens!".format(name, num))

    db.session.commit()
    return redirect("/?alert_type=failure&alert={}".format("Incorrect"))

@login_required
@app.route('/js/<remainder>',methods=['GET'])
@app.route('/img/<remainder>',methods=['GET'])
def get_static(remainder):
    return send_from_directory(app.static_folder,request.path[1:])

if __name__ == "__main__":
    app.run(host="0.0.0")
