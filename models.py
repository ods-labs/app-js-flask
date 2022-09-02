from . import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)
    postits = db.relationship('Postit', backref='users')

class Postit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=True)
    publish = db.Column(db.Boolean, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
