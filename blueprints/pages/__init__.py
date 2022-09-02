from flask import Blueprint
from flask import render_template, make_response, redirect
from application import decorators

bp = Blueprint('pages', __name__)

@bp.get("/")
@decorators.check_token
def base(user):
    return render_template('index.html', user=user)

@bp.get('/register')
def register():
    return render_template('register.html')

@bp.get("/login")
def login():
    return render_template('login.html')

@bp.get("/logout")
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('session_id')
    return resp