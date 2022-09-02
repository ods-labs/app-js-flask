from jwt import DecodeError
from functools import wraps
import jwt
from flask import request, make_response
from .models import Users
from flask import current_app as app

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return make_response({'status':'failed', 'message': 'A valid token is missing'}, 401)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = Users.query.filter_by(public_id=data['public_id']).first() # TODO: check if token expired data['exp']
        except DecodeError as err:
            return make_response({'status':'failed', 'message': 'A valid token is missing, %s' % str(err)}, 401)
        return f(current_user, *args, **kwargs)
    return decorator

def check_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if 'session_id' in request.cookies:
            token = request.cookies['session_id']
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
