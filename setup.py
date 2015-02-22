from server import db, create_user, model

db.create_all()

a = model.Lichen("wolfeyes", "Wolf Eyes", "/static/img/lichen_wolf_eyes.jpg")
a.description = "The wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thattttttttttttThe wolf eyes does this and this and that"
b = model.Lichen("bryoria", "Bryoria", "/static/img/bryoria.jpg")
a.description = "The Bryoria does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thattttttttttttThe wolf eyes does this and this and that"
c = model.Lichen("cribellifrum", "Cribellifrum", "/static/img/cribellifrum.jpg")
a.description = "The cribellifrum does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thattttttttttttThe wolf eyes does this and this and that"

db.session.add(a)
db.session.add(b)
db.session.add(c)

a = model.Clue("The lichen is located in a green building", 1)
b = model.Clue("The lichen is located in a pink",2)
c = model.Clue("The lichen is located in a blue building", 3)

db.session.add(a)
db.session.add(b)
db.session.add(c)

db.session.commit()

create_user('admin', 'password')
