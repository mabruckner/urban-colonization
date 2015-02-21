from flask import *
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/fhb.db'

app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/makeuser', methods=['GET'])
def makeuser():
    admin = User('admin', 'admin@example.com')
    db.session.add(admin)
    db.session.commit()
    return ""

@app.route('/getuser', methods=['GET'])
def getuser():
    admin = User.query.filter_by(username='admin').first()
    return admin.username

@app.route('/', methods=['GET'])
def hello():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0")