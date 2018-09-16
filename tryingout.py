import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pprint
import json

if len(sys.argv) > 1:
    search_str = sys.argv[1]
else:
    search_str = 'Radiohead'

client_id = "8cf3536e2878430ba6f2ae0755ddcfcf"
client_secret = "9ee29828e6da477aa6fc06ed219f4923"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

result = sp.search(search_str)

result_one_name = result['tracks']['items'][0]['name']
print(result_one_name)

with open('data.json', 'w') as outfile:
    json.dump(result, outfile)