from flask_table import Table, Col
 
class Results(Table):
    id = Col('id', show=False)
    artist = Col('artist')
    title = Col('title')
    """
    release_date = Col('Release Date')
    publisher = Col('Publisher')
    media_type = Col('Media')
    """