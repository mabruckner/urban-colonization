from server import db, create_user, model

db.create_all()

a = model.Clue("The lichen is located in a green building", 1)
b = model.Clue("The lichen is located in a pink",2)
c = model.Clue("The lichen is located in a blue building", 3)

db.session.add(a)
db.session.add(b)
db.session.add(c)

db.session.commit()

create_user('admin', 'password')
