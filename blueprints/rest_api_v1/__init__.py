from flask import Blueprint
from flask import request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import datetime
import jwt

from application.models import Users, Postit
from application.decorators import check_token, token_required
from application import db
from flask import current_app as app

bp = Blueprint('rest_api_v1', __name__)

@bp.post('/register')
def signup_user():
    data = request.get_json()
    if not data['username']:
        return {
            'status':'ko',
            'message':'Username is missing'
        }

    if not data['password'] or data['password'] != data['passwordcheck']:
        return {
            'status':'ko',
            'message':'Password missing or mismatch'
        }

    user = Users.query.filter_by(name=data['username']).first()
    if user:
        return {
            'status':'ko',
            'message':'Username already in use, try another one'
        }

    hashed_password = generate_password_hash(data['password'], method='sha256')
    try:
        new_user = Users(public_id=str(uuid.uuid4()), name=data['username'], password=hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()
    except:
        return {
            'status':'ko',
            'message':'Something went wrong with the back, try to stretch and relax'
        }
    return {
        'status':'ok',
        'message':'User created successfully'
    }

@bp.post('/login')
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response({'status':'failed', 'message': 'Basic auth missing'}, 401)

    user = Users.query.filter_by(name=auth.username).first()

    if user and check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=1)},
                           app.config['SECRET_KEY'],
                           algorithm='HS256')
        return {'token' : token}

    return make_response({'status':'failed', 'message': 'User not found, or wrong password'},  401)

@bp.get("/api")
@check_token
def get_api(user):
    rows = Postit.query.all()
    ret = []
    for row in rows:
        if not (user and user.admin) and not row.publish:
            continue
        output = dict()
        output['id'] = row.id
        output['title'] = row.title
        output['description'] = row.description
        if user and (user.id == row.user_id or user.admin):
            output['delete'] = True
        if user and user.admin:
            output['publish'] = row.publish
        ret.append(output)
    return {'data': ret}

@bp.post("/api")
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

@bp.put("/api/<id>")
@token_required
def update_api(user, id):
    postit = None
    if user.admin:
        postit = Postit.query.filter_by(id=id).first()
    else:
        postit = Postit.query.filter_by(id=id, user_id=user.id).first()
    if postit:
        postit.publish = request.json['publish']
        db.session.commit()
        return {'status':'ok'}
    else:
        return {'status':'failed'}

@bp.delete("/api/<id>")
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
