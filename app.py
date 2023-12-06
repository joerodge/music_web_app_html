import os
from flask import Flask, request, redirect, render_template
from lib.database_connection import get_flask_database_connection
from lib.album_repository import AlbumRepository
from lib.album import Album
from lib.artist_repository import ArtistRepository
from lib.artist import Artist
# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==


# == Example Code Below ==

# GET /emoji
# Returns a smiley face in HTML
# Try it:
#   ; open http://localhost:5001/emoji
@app.route('/emoji', methods=['GET'])
def get_emoji():
    # We use `render_template` to send the user the file `emoji.html`
    # But first, it gets processed to look for placeholders like {{ emoji }}
    # These placeholders are replaced with the values we pass in as arguments
    return render_template('emoji.html', emoji=':)')

# 

@app.route('/albums', methods=['GET'])
def get_albums():
    connection = get_flask_database_connection(app)
    album_repo = AlbumRepository(connection)
    albums = album_repo.all()
    return render_template('albums/albums.html', albums_list=albums)

@app.route('/albums/<id>')
def get_1_album(id):
    connection = get_flask_database_connection(app)
    album_repo = AlbumRepository(connection)
    album = album_repo.find(id)
    artist_repo = ArtistRepository(connection)
    artist = artist_repo.find(album.artist_id)
    return render_template('albums/album_single.html', album=album, artist=artist)

@app.route('/artists', methods=['GET'])
def get_artists():
    connection = get_flask_database_connection(app)
    artist_repo = ArtistRepository(connection)
    artists = artist_repo.all()
    return render_template('artists/artists.html', artists=artists)


@app.route('/artists/<id>')
def get_1_artist(id):
    connection = get_flask_database_connection(app)
    artist_repo = ArtistRepository(connection)
    artist = artist_repo.find(id)
    return render_template('artists/artist_single.html', artist=artist)

@app.route('/albums/new', methods=['GET'])
def new_album():
    return render_template('albums/new.html')


@app.route('/albums', methods=['POST'])
def create_new_album():
    connection = get_flask_database_connection(app)
    album_repo = AlbumRepository(connection)
    title = request.form['title']
    release_year = request.form['release_year']
    artist_id = request.form['artist_id']
    if not title or not release_year or not artist_id:
        return render_template('albums/new.html', error="Error: One or more field was empty")
    
    id = album_repo.create(title, release_year, artist_id)
    return redirect(f'/albums/{id}')

@app.route('/artists/new', methods=['GET'])
def new_artist():
    return render_template('artists/new.html')

@app.route('/artists', methods=['POST'])
def create_new_artist():
    connection = get_flask_database_connection(app)
    artist_repo = ArtistRepository(connection)
    artist_name = request.form['artist_name']
    genre = request.form['genre']
    if not artist_name or not genre:
        return render_template('artists/new.html', error="Error: One or more field was empty")
    
    artist = Artist(None, artist_name, genre)
    id = artist_repo.create(artist)
    return redirect(f"/artists/{id}")

# This imports some more example routes for you to see how they work
# You can delete these lines if you don't need them.
from example_routes import apply_example_routes
apply_example_routes(app)

# == End Example Code ==

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))

