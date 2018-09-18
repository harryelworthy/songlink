import functools

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response, abort
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

@bp.route('/<uri>/', methods=['GET'])
def relink(uri):
    url = generate_link(uri, 1)
    if not url:
        abort(400, 'No song found')
    return make_response(redirect(url))


def add_spotify_results_db(result):
    # Need to make loop through all results
    for item in result['tracks']['items']:
        name = item['name']
        artist = item['artists'][0]['name']
        album = item['album']['name']
        uri = item['id']
        add_to_db(name, artist, album, uri)
        print(name)
    return

def add_to_db(name, artist, album, uri):
    db = get_db()
    if db.execute('SELECT uri FROM song WHERE uri = ?', (uri,)).fetchone() is None:
        db.execute(
            'INSERT INTO song (title, artist, album, uri) VALUES (?, ?, ?, ?)', (name, artist, album, uri)
        )
    db.commit()
    return

def generate_link(uri, pref):
    link = None
    db = get_db()
    if db.execute(
            'SELECT uri FROM song WHERE uri = ?', (uri,)
        ).fetchone() is None:
        return None

    if pref == 1:
        link = "https://open.spotify.com/track/" + uri
    return link

@bp.route('/firsttime')
def first_time(songid):
	resp = make_response(render_template('/song/firsttime.html', songid))
	# Get Preference
	# Create new user, set preference, get ID
	resp.set_cookie('user', userid)
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
        results = db.execute(
            "SELECT * FROM song WHERE (artist LIKE '%" + search_string + "%') OR (album LIKE '%" + search_string + "%') OR (title LIKE '%" + search_string + "%')"
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

