from server import db, create_user, model

db.create_all()

a = model.Lichen("wolfeyes", "Wolf Eyes", "/static/img/lichen_wolf_eyes.jpg")
a.description = "The 'brown eyes' are the fruiting bodies where spores are made for reproduction.  The lichen is a combination of fungus and algae (or, sometimes, cyanobacteria), but only the fungal partner reproduces sexually and produces spores - then the new generation has to find its algal partner all over again.  Wolf lichens are so named because of their common use as poisons for wolves and foxes in Europe centuries ago. The lichen, with its toxic vulpinic acid, was mixed with ground glass and meat, apparently a deadly combination."
b = model.Lichen("bryoria", "Bryoria", "/static/img/bryoria.jpg")
b.description = "Wila (Bryoria fremontii), like almost all of the 23 other species of Bryoria found in North America, is a dark brown hair lichen that grow on trees (mostly conifers). Differentiating the different species of Bryoria can be difficult. The simplest characteristic that distinguishes wila from the other species of Bryoria is that its main branches grow to be quite thick (greater than 0.4 mm wide), and usually become somewhat flattened, twisted, and wrinkled in older specimens. Other species of Bryoria usually have narrower main branches. Wila can also grow to be a lot longer than other species of Bryoria, and is the only species in this genus in North America that regularly grows longer than 20 cm (occasionally reaching 90 cm in length). Wila is often slightly darker in colour than most other species of Bryoria, although there is much variation in this characteristic. Soredia and apothecia are uncommon, but when they are present they are very distinctive, as they are both bright yellow."
c = model.Lichen("cribellifrum", "Cribellifrum", "/static/img/cribellifrum.jpg")
c.description = "Is this a fake lichen?"

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
