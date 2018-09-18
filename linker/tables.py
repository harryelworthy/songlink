from flask_table import Table, Col
 
class Results(Table):
    id = Col('id')
    artist = Col('artist')
    title = Col('title')
    album = Col('album')
    uri = Col('uri')
    """
    release_date = Col('Release Date')
    publisher = Col('Publisher')
    media_type = Col('Media')
    """