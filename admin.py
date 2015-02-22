from flask import *
from flask.ext.sqlalchemy import SQLAlchemy

from Model import Model

app = Flask(__name__)

model = Model(app)
db = model.db
User = model.User
Clue = model.Clue
Lichen = model.Lichen

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/uc.db'
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/', methods=['GET'])
def hello():
    return render_template('admin/admin.html')

@app.route('/addclue', methods=['GET'])
def addclue():
    return render_template('admin/addclue.html')

@app.route('/submitclue', methods=['GET'])
def submitclue():
    clue = Clue(request.args.get('clue'), request.args.get('lichenid'))
    db.session.add(clue)
    db.session.commit()
    return redirect("/viewclues")

@app.route('/viewclues', methods=['GET'])
def viewclues():
    s = ["id, text, target"]
    for x in Clue.query.all():
        s.append(str(x))
    return "<br/>".join(s)

@app.route('/addlichen', methods=['GET'])
def addlichen():
    return render_template('admin/addlichen.html')

@app.route('/submitlichen', methods=['GET'])
def submitlichen():
    lichen = Lichen(request.args.get('name'), request.args.get('imgpath'))
    db.session.add(lichen)
    db.session.commit()
    return redirect("/viewlichens")

@app.route('/viewlichens', methods=['GET'])
def viewlichens():
    s = ["id, name, image, desc"]
    for x in Lichen.query.all():
        s.append(str(x))
    return "<br/>".join(s)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
