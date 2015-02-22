from server import db, create_user, model

db.create_all()

a = model.Lichen("wolfeyes", "Wolf Eyes", "/static/img/lichen_wolf_eyes.jpg")
a.description = "The 'brown eyes' are the fruiting bodies where spores are made for reproduction.  The lichen is a combination of fungus and algae (or, sometimes, cyanobacteria), but only the fungal partner reproduces sexually and produces spores - then the new generation has to find its algal partner all over again.  Wolf lichens are so named because of their common use as poisons for wolves and foxes in Europe centuries ago. The lichen, with its toxic vulpinic acid, was mixed with ground glass and meat, apparently a deadly combination."
a.passcode = "passcode"
a.hint = "This can be found hanging high above with a sunny disposition. They were named in Latin for their split-end appearance."
db.session.add(a)

a = model.Lichen("bryoria", "Bryoria", "/static/img/bryoria.jpg")
a.description = "Wila (Bryoria fremontii), like almost all of the 23 other species of Bryoria found in North America, is a dark brown hair lichen that grow on trees (mostly conifers). Differentiating the different species of Bryoria can be difficult. The simplest characteristic that distinguishes wila from the other species of Bryoria is that its main branches grow to be quite thick (greater than 0.4 mm wide), and usually become somewhat flattened, twisted, and wrinkled in older specimens. Other species of Bryoria usually have narrower main branches. Wila can also grow to be a lot longer than other species of Bryoria, and is the only species in this genus in North America that regularly grows longer than 20 cm (occasionally reaching 90 cm in length). Wila is often slightly darker in colour than most other species of Bryoria, although there is much variation in this characteristic. Soredia and apothecia are uncommon, but when they are present they are very distinctive, as they are both bright yellow."
a.passcode = "passcode"
a.hint = "Do finding these colonies have you stumped...literally?"
db.session.add(a)

a = model.Lichen("parientina", "Maritime Sunburst Lichen", "/static/img/parientina.jpg")
a.description = "The outer 'skin' of the lichen, the cortex, is composed of closely packed fungal hyphae and serves to protect the thallus from water loss due to evaporation as well as harmful effects of high levels of irradiation. In Xanthoria parietina, the thickness of the thalli is known to vary depending on the habitat is which it grows. Thalli are much thinner in shady locations than in those exposed to full sunshine; this has the effect of protecting the algae that cannot tolerate high light intensities. The lichen pigment parietin gives this species a deep yellow or orange-red color."
a.passcode = "passcode"
a.hint = "Adept in the art of camouflage, this lichen you 'wood' not see otherwise."
db.session.add(a)

a = model.Lichen("parmotrema", "Scatter-Rag Lichens", "/static/img/parmotrema.jpg")
a.description = "Ascospores are simple, hyaline, and often small. Conidia generally arise laterally from the joints of conidiogenous hyphae (Parmelia-type), but arise terminally from these joints in a small number of species (Psora-type). The conidia can have a broad range of shapes: cylindrical to bacilliform, bifusiform, fusiform, sublageniform, unciform, filiform, or curved. Pycnidia are immersed or rarely emergent from the upper cortex, are produced along the lamina or margins, pyriform in shape, and dark-brown to black in colour.[6]"
a.passcode = "passcode"
a.hint = "Long, silvery-green, tendril like ruffles welcome the public and 'shields' all  those who enter."
db.session.add(a)

a = model.Lichen("unidentified", "Unidentified", "/static/img/unidentified.jpg")
a.description = "Is this a fake lichen?"
a.passcode = "passcode"
a.hint = "We found a hidden niche where soldiers, pixies and reindeer cohabitate  beautifully."
db.session.add(a)

a = model.Lichen("cladonia", "Cup Lichen", "/static/img/cladonia.jpg")
a.description = "Cladonia (cup lichen) is a genus of moss-like lichens in the family Cladoniaceae. They are the primary food source for reindeer and caribou. Cladonia species are of economic importance to reindeer-herders, such as the Sami in Scandinavia or the Nenets in Russia. Antibiotic compounds are extracted from some species to create antibiotic cream. The light green species Cladonia stellaris is used in flower decorations."
a.passcode = "passcode"
a.hint = "Growing low and facing West, these golden gems glow. They can be found  rockin' it--metal style."
db.session.add(a)

a = model.Lichen("farinaceae", "Cup Lichen", "/static/img/farinaceae.jpg")
a.description = "Cladonia (cup lichen) is a genus of moss-like lichens in the family Cladoniaceae. They are the primary food source for reindeer and caribou. Cladonia species are of economic importance to reindeer-herders, such as the Sami in Scandinavia or the Nenets in Russia. Antibiotic compounds are extracted from some species to create antibiotic cream. The light green species Cladonia stellaris is used in flower decorations."
a.passcode = "passcode"
a.hint = "Capable of thriving on inhospitable surfaces, this particular specimen has a hobby of hanging out near windows."
db.session.add(a)

db.session.commit()

create_user('admin', 'admin@example.com', 'password')
