from playwright.sync_api import Page, expect
from lib.album import Album
from lib.album_repository import AlbumRepository

# Tests for your routes go here

# === Example Code Below ===

"""
We can get an emoji from the /emoji page
"""
def test_get_emoji(page, test_web_address): # Note new parameters
    # We load a virtual browser and navigate to the /emoji page
    page.goto(f"http://{test_web_address}/emoji")

    # We look at the <strong> tag
    strong_tag = page.locator("strong")

    # We assert that it has the text ":)"
    expect(strong_tag).to_have_text(":)")

# === End Example Code ===

def test_get_albums(page, test_web_address, db_connection):
    db_connection.seed('seeds/music.sql')
    page.goto(f"http://{test_web_address}/albums")
    div_tags = page.locator("div")
    expect(div_tags).to_have_text([
                "Doolittle \nReleased: 1989",
                "Surfer Rosa \nReleased: 1988",
                "Waterloo \nReleased: 1974",
                "Super Trouper \nReleased: 1980",
                "Bossanova \nReleased: 1990",
                "Lover \nReleased: 2019",
                "Folklore \nReleased: 2020",
                "I Put a Spell on You \nReleased: 1965",
                "Baltimore \nReleased: 1978",
                "Here Comes the Sun \nReleased: 1971",
                "Fodder on My Wings \nReleased: 1982",
                "Ring Ring \nReleased: 1973",
    ])

def test_get_single_album(page, test_web_address, db_connection):
    db_connection.seed('seeds/music.sql')
    page.goto(f"http://{test_web_address}/albums/6")
    h1_tag = page.locator('h1')
    p_tags = page.locator('p')
    expect(h1_tag).to_have_text('Lover')
    expect(p_tags).to_have_text([
        'Release year: 2019',
        'Artist: Taylor Swift'
    ])
    

def test_getting_all_artist(page, test_web_address, db_connection):
    db_connection.seed('seeds/music.sql')
    page.goto(f"http://{test_web_address}/artists")
    h1_tag = page.locator('h1')
    p_tags = page.locator('p')
    expect(h1_tag).to_have_text([
        'Pixies',
        'ABBA',
        'Taylor Swift',
        'Nina Simone',
    ])
    expect(p_tags).to_have_text(['Genre: Rock','Genre: Pop','Genre: Pop','Genre: Jazz'])


def test_get_single_artist(page, test_web_address, db_connection):
    db_connection.seed('seeds/music.sql')
    page.goto(f"http://{test_web_address}/artists/2")
    h1_tag = page.locator('h1')
    p_tag = page.locator('p')
    expect(h1_tag).to_have_text('ABBA')
    expect(p_tag).to_have_text('Genre: Pop')


def test_create_new_album(page, test_web_address, db_connection):
    page.set_default_timeout(2000)
    db_connection.seed('seeds/music.sql')
    page.goto(f"http://{test_web_address}/albums")
    page.click("text='Create a new album'")
    page.fill("input[name=title]", "Test Album")
    page.fill("input[name=release_year]", "1999")
    page.fill("input[name=artist_id]", "3")
    page.click("text='Add album'")
    h1_tag = page.locator('h1')
    p_tags = page.locator('p')
    expect(h1_tag).to_have_text('Test Album')
    expect(p_tags).to_have_text([
        'Release year: 1999',
        'Artist: Taylor Swift'
    ])


def test_create_album_when_input_fields_are_incorrect(page, test_web_address, db_connection):
    page.set_default_timeout(2000)
    db_connection.seed('seeds/music.sql')
    page.goto(f"http://{test_web_address}/albums")
    page.click("text='Create a new album'")
    page.click("text='Add album'")
    errors_tag = page.locator(".t-errors")
    expect(errors_tag).to_have_text("Error: One or more field was empty")


def test_add_new_artist(page, test_web_address, db_connection):
    page.set_default_timeout(2000)
    db_connection.seed('seeds/music.sql')
    page.goto(f"http://{test_web_address}/artists")
    page.click("text='Create a new artist'")
    page.fill("input[name=artist_name]", "Test Artist")
    page.fill("input[name=genre]", "test genre")
    page.click("text='Add artist'")
    h1_tag = page.locator('h1')
    p_tag = page.locator('p')
    expect(h1_tag).to_have_text('Test Artist')
    expect(p_tag).to_have_text('Genre: test genre')

def test_add_new_artist_with_blank_fields(page, test_web_address, db_connection):
    page.set_default_timeout(2000)
    db_connection.seed('seeds/music.sql')
    page.goto(f"http://{test_web_address}/artists")
    page.click("text='Create a new artist'")
    # Don't fill in text and click submit while they are empty
    page.click("text='Add artist'")
    errors_tag = page.locator(".t-errors")
    expect(errors_tag).to_have_text("Error: One or more field was empty")