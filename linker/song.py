import functools

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db, init_db

from .forms import MusicSearchForm

from .tables import Results

bp = Blueprint('song', __name__, url_prefix='/s')

client_id = "8cf3536e2878430ba6f2ae0755ddcfcf"
client_secret = "9ee29828e6da477aa6fc06ed219f4923"


def get_spotify_results(search):
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp.search(search)



def add_spotify_results_db(result):
    # Need to make loop through all results
    for item in result['tracks']['items']:
        name = result['tracks']['items'][0]['name']
        artist = result['tracks']['items'][0]['artists'][0]['name']
        album = result['tracks']['items'][0]['album']['name']
        url = result['tracks']['items'][0]['uri']
        add_to_db(name, artist, album, url)
    return

def add_to_db(name, artist, album, sp_url):
    db = get_db()
    db.execute(
        'INSERT INTO song (title, artist, album, spotify, link, type)'
        ' VALUES (?, ?, ?, ?, ?, ?)',
        (name, artist, album, sp_url, 0, '')
    )
    db.commit()
    return

def generate_link(songlink, pref):
	link = None
	if pref == 1:
		link = db.execute('SELECT spotify FROM song WHERE link = ?', (songlink,)).fetchone()
	return link

@bp.route('/firsttime')
def first_time(songid):
	resp = make_response(render_template('/song/firsttime.html', songid))
	# Get Preference
	# Create new user, set preference, get ID
	resp.set_cookie('user', userid)
	return resp

@bp.route('/<songlink>')
def relink(songlink):
    # Redirect user to their link of choice
    resp = make_response(None)

    link = generate_link(songlink, 1)
    resp = make_response(redirect(link))

    return resp




@bp.route('/search', methods=['GET', 'POST'])
def search_page():
    search = MusicSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search)

@bp.route('/results')
def search_results(search):
    db = get_db()
    results = []
    search_string = search.data['search']
    if True: #search.data['search'] == ''
        spsearch = get_spotify_results(search_string)
        add_spotify_results_db(spsearch)
        radiohead = 'radiohead'
        results = db.execute(
            "SELECT * FROM song"
            "WHERE (artist LIKE 'radiohead')"
            "OR (album LIKE 'radiohead')"
        )

        #results = ['hello']

    if not results:
        flash('No results found!')
        return redirect('/a')
    else:
        # display results        
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)

