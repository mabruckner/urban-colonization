from server import db, create_user, model

db.create_all()

a = model.Lichen("wolfeyes", "Wolf Eyes", "/static/img/lichen_wolf_eyes.jpg")
a.description = "The wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thattttttttttttThe wolf eyes does this and this and that"
b = model.Lichen("bryoria", "Bryoria", "/static/img/bryoria.jpg")
b.description = "The Bryoria does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thattttttttttttThe wolf eyes does this and this and that"
c = model.Lichen("cribellifrum", "Cribellifrum", "/static/img/cribellifrum.jpg")
c.description = "The cribellifrum does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thaThe wolf eyes does this and this and thattttttttttttThe wolf eyes does this and this and that"

db.session.add(a)
db.session.add(b)
db.session.add(c)

clues = [
    model.Clue("This can be found hanging high above with a sunny disposition. They were named in Latin for their split-end appearance.", 1),
    model.Clue("Do finding these colonies have you stumped...literally?", 1),
    model.Clue("Adept in the art of camouflage, this lichen you 'wood' not see otherwise.", 1),
    model.Clue("Long, silvery-green, tendril like ruffles welcome the public and 'shields' all  those who enter.", 1),
    model.Clue("We found a hidden niche where soldiers, pixies and reindeer cohabitate  beautifully.", 1),
    model.Clue("Growing low and facing West, these golden gems glow. They can be found  rockin' it--metal style.", 1),
    model.Clue("Capable of thriving on inhospitable surfaces, this particular specimen has a hobby of hanging out near windows.", 1)
]

map(db.session.add, clues)

db.session.commit()

create_user('admin', 'password')
