import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('song', __name__, url_prefix='/s')

@bp.route('/<songlink>')
def relink(songlink):
    # show the user profile for that user
    resp = make_response(None)
    if request.method == 'POST':
        db = get_db()
        error = None
        try: 
        	cookie = request.cookies.get('user')

    	except: 
    		cookie = None

    	if cookie != None:
    		pref = db.execute('SELECT preference FROM user WHERE cookie = ?', (cookie,)).fetchone()
    		link = generate_link(songlink, pref)
    		resp = make_response(redirect(link))
    	else:
    		resp = make_response(redirect(url_for('first_time')))
    return resp

@app.route('/')
def index():
    username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.
Storing cookies:

from flask import make_response

@app.route('/')
def index():
    resp = make_response(render_template(...))
    resp.set_cookie('username', 'the username')
    return resp

def generate_link(songlink, pref):
	link = None
	if pref = 1:
		link = db.execute('SELECT spotify FROM song WHERE link = ?', (songlink,)).fetchone()
	return link

@bp.route('/firsttime')
def first_time(songid):
	resp = make_response(render_template('/song/firsttime.html', songid))
	# Get Preference
	# Create new user, set preference, get ID
	resp.set_cookie('user', userid)
	return resp