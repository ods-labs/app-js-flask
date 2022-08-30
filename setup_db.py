from app import db, Postit

db.drop_all()
db.create_all()
postitA = Postit(title='Hello', description='World')
postitB = Postit(title='Bonjour', description='Le monde')
db.session.add(postitA)
db.session.add(postitB)
db.session.commit()