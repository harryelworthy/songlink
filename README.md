# Songlink - Working Title (could be working harder)
## A light web app to make linking songs easy. Users' redirect preferences are saved to cookies, so that each person gets redirected to their chosen service

This should ideally be a one-interaction site. First song I click, I pick my streaming choice, then every time after I get that service. Main site I can change my preferences. DB of song links is obviously key, Spotify/AM etc API's can work with this. Search page also key. 

Going to use flask to first mock up, as I have a bit of experience there and it's small and simple, should probably use something .js or rails or whatever the cool kids are using if I really want to build this. Not too important right now. How tough can a three function site be?!

To Do:

JUST SPOTIFY TO START
* Set up Flask simple working locally
* Set up databases (ask ted? Or google for simplest small) for:
** User Profiles (cookies id) with preferences
** Song Links - sl id + spotify link, am link etc, + name, artist, album, etc
** Data of what happens
* Set up Spotipy script to search when search comes in - search spotipy, take first result, add SL database
* Set up script for when click on link, log cookies, set preference, link on