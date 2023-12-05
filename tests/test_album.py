from lib.album import Album

def test_album_object_created_correctly():
    album = Album(1, 'Test Album', 1995, 3)
    assert album.id == 1
    assert album.title == 'Test Album'
    assert album.release_year == 1995
    assert album.artist_id == 3


def test_equal_obects():
    album1 = Album(1, 'Test Album', 1995, 3)
    album2 = Album(1, 'Test Album', 1995, 3)
    assert album1 == album2


def test_repr():
    album1 = Album(1, 'Test Album', 1995, 3)
    assert str(album1) == "Album(1, Test Album, 1995, 3)"