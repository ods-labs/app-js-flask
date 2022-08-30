import uuid
import jwt
from jwt import DecodeError
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY']='Th1s1ss3cr3t'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/frederic/Documents/cours-fullstack/identifier.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return {'message': 'a valid token is missing'}
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = Users.query.filter_by(public_id=data['public_id']).first() # TODO: check if token expired data['exp']
        except DecodeError as err:
            return {'message': 'token is invalid', 'reason': str(err)}
        return f(current_user, *args, **kwargs)
    return decorator

def check_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if token:
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                current_user = Users.query.filter_by(public_id=data['public_id']).first()
            except DecodeError:
                return f(None, *args, **kwargs)
            return f(current_user, *args, **kwargs)
        else:
            return f(None, *args, **kwargs)
    return decorator


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def signup_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return {'message': 'registered successfully'}

@app.route('/login', methods=['GET', 'POST'])
def login_user():

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = Users.query.filter_by(name=auth.username).first()

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'],
                           algorithm='HS256')
        return {'token' : token}

    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.get("/api")
@check_token
def get_api(user):
    rows = Postit.query.all()
    ret = []
    for row in rows:
        output = dict()
        output['id'] = row.id
        output['title'] = row.title
        output['description'] = row.description
        if user and (user.id == row.user_id or user.admin):
            output['publish'] = row.publish
        ret.append(output)
    return {'data': ret}

@app.post("/api")
@token_required
def post_api(user):
    postit = Postit(
        title=request.json['title'],
        description=request.json['description'],
        publish=False,
        user_id=user.id)
    db.session.add(postit)
    db.session.commit()
    return {'status':'ok'}

@app.delete("/api/<id>")
@token_required
def delete_api(user, id):
    postit = None
    if user.admin:
        postit = Postit.query.filter_by(id=id).first()
    else:
        postit = Postit.query.filter_by(id=id, user_id=user.id).first()
    if postit:
        db.session.delete(postit)
        db.session.commit()
        return {'status':'ok'}
    else:
        return {'status':'failed'}
