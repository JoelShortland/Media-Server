"""
Route management.
This provides all of the websites routes and handles what happens each
time a browser hits each of the paths. This serves as the interaction
between the browser and the database while rendering the HTML templates
to be displayed.
You will have to make
"""

# Importing the required packages
import hashlib
import uuid
from modules import *
from flask import *
import database

user_details = {}  # User details kept for us
session = {}  # Session information (logged in state)
page = {}  # Determines the page information
contact_details = {}

# Initialise the application
app = Flask(__name__)
app.secret_key = """U29tZWJvZHkgb25jZSB0b2xkIG1lIFRoZSB3b3JsZCBpcyBnb25uYSBy
b2xsIG1lIEkgYWluJ3QgdGhlIHNoYXJwZXN0IHRvb2wgaW4gdGhlIHNoZWQgU2hlIHdhcyBsb29r
aW5nIGtpbmRhIGR1bWIgV2l0aCBoZXIgZmluZ2VyIGFuZCBoZXIgdGh1bWIK"""


#####################################################
#   INDEX
#####################################################

@app.route('/')
def index():
    """
    Provides the main home screen if logged in.
        - Shows user playlists
        - Shows user Podcast subscriptions
        - Shows superUser status
    """
    # Check if the user is logged in, if not: back to login.
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'User Management'

    # Get a list of user playlists
    user_playlists = None
    user_playlists = database.user_playlists(user_details['username'])
    # Get a list of subscribed podcasts
    user_subscribed_podcasts = None
    user_subscribed_podcasts = database.user_podcast_subscriptions(user_details['username'])
    # Get a list of in-progress items
    user_in_progress_items = None
    user_in_progress_items = database.user_in_progress_items(user_details['username'])
    # Data integrity checks
    if user_playlists == None:
        user_playlists = []

    if user_subscribed_podcasts == None:
        user_subscribed_podcasts = []

    if user_in_progress_items == None:
        user_in_progress_items = []

    return render_template('index.html',
                           session=session,
                           page=page,
                           user=user_details,
                           playlists=user_playlists,
                           subpodcasts=user_subscribed_podcasts,
                           usercurrent=user_in_progress_items)


#####################################################
#####################################################
####    User Management
#####################################################
#####################################################

#####################################################
#   LOGIN
#####################################################

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        global user_details
        global contact_details
        # submitting details
        # The form gives back EmployeeID and Password
        salt = database.get_salt(request.form['username'])[0]['salt']
        print("salt is: ", salt)
        if salt is None:
            login_return_data = database.check_login_unsafe(
                request.form['username'],
                request.form['password'])

            if login_return_data is None:
                page['bar'] = False
                flash("Incorrect username/password, please try again")
                return redirect(url_for('login'))

                # If there was no error, log them in
            page['bar'] = True
            flash('You have been logged in successfully. Your details are not secure,'
                  ' please change your password in the account tab!')
            session['logged_in'] = True
            user_details = login_return_data[0]
            contact_details = database.get_contact_details(user_details['username'])
            return redirect(url_for('index'))

        login_return_data = database.check_login(
            request.form['username'],
            request.form['password'],
            salt
        )

        # If it's null, saying they have incorrect details
        if login_return_data is None:
            page['bar'] = False
            flash("Incorrect username/password, please try again")
            return redirect(url_for('login'))

        # If there was no error, log them in
        page['bar'] = True
        flash('You have been logged in successfully')
        session['logged_in'] = True

        # Store the user details for us to use throughout
        user_details = login_return_data[0]
        contact_details = database.get_contact_details(user_details['username'])

        return redirect(url_for('index'))

    elif request.method == 'GET':
        return render_template('login.html', session=session, page=page)


#####################################################
#   LOGOUT
#####################################################

@app.route('/logout')
def logout():
    """
    Logs out of the current session
        - Removes any stored user data.
    """
    session['logged_in'] = False
    page['bar'] = True
    flash('You have been logged out')
    return redirect(url_for('index'))


#####################################################
#####################################################
####    List All items
#####################################################
#####################################################


#####################################################
#   List Artists
#####################################################
@app.route('/list/artists')
def list_artists():
    """
    Lists all the artists in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Artists'

    # Get a list of all artists from the database
    allartists = None
    allartists = database.get_allartists()

    # Data integrity checks
    if allartists == None:
        allartists = []

    return render_template('listitems/listartists.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allartists=allartists)


#####################################################
#   List Songs
#####################################################
@app.route('/list/songs')
def list_songs():
    """
    Lists all the songs in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Songs'

    # Get a list of all songs from the database
    allsongs = None
    allsongs = database.get_allsongs()

    # Data integrity checks
    if allsongs == None:
        allsongs = []

    return render_template('listitems/listsongs.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allsongs=allsongs)


#####################################################
#   List Podcasts
#####################################################
@app.route('/list/podcasts')
def list_podcasts():
    """
    Lists all the podcasts in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List podcasts'

    # Get a list of all podcasts from the database
    allpodcasts = None
    allpodcasts = database.get_allpodcasts()

    # Data integrity checks
    if allpodcasts == None:
        allpodcasts = []

    return render_template('listitems/listpodcasts.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allpodcasts=allpodcasts)


#####################################################
#   List Movies
#####################################################
@app.route('/list/movies')
def list_movies():
    """
    Lists all the movies in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Movies'

    # Get a list of all movies from the database
    allmovies = None
    allmovies = database.get_allmovies()

    # Data integrity checks
    if allmovies == None:
        allmovies = []

    return render_template('listitems/listmovies.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allmovies=allmovies)


#####################################################
#   List Albums
#####################################################
@app.route('/list/albums')
def list_albums():
    """
    Lists all the albums in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Albums'

    # Get a list of all Albums from the database
    allalbums = None
    allalbums = database.get_allalbums()

    # Data integrity checks
    if allalbums == None:
        allalbums = []

    return render_template('listitems/listalbums.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allalbums=allalbums)


#####################################################
#   List TVShows
#####################################################
@app.route('/list/tvshows')
def list_tvshows():
    """
    Lists all the tvshows in your media server
    Can do this without a login
    """

    # # Check if the user is logged in, if not: back to login.
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'List TV Shows'

    # Get a list of all tvshows from the database
    alltvshows = None
    alltvshows = database.get_alltvshows()

    # Data integrity checks
    if alltvshows == None:
        alltvshows = []

    return render_template('listitems/listtvshows.html',
                           session=session,
                           page=page,
                           user=user_details,
                           alltvshows=alltvshows,
                           contact=contact_details)


#####################################################
#####################################################
####    List Individual items
#####################################################
#####################################################

#####################################################
#   Individual Artist
#####################################################
@app.route('/artist/<artist_id>')
def single_artist(artist_id):
    """
    Show a single artist by artist_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'Artist ID: ' + artist_id

    # Get a list of all artist by artist_id from the database
    artist = None
    artist = database.get_artist(artist_id)

    # Data integrity checks
    if artist == None:
        artist = []

    return render_template('singleitems/artist.html',
                           session=session,
                           page=page,
                           user=user_details,
                           artist=artist)


#####################################################
#   Individual Song
#####################################################
@app.route('/song/<song_id>')
def single_song(song_id):
    """
    Show a single song by song_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'Song'

    # Get a list of all song by song_id from the database
    song = None
    song = database.get_song(song_id)

    songmetadata = None
    songmetadata = database.get_song_metadata(song_id)

    # Data integrity checks
    if song == None:
        song = []

    if songmetadata == None:
        songmetadata = []

    return render_template('singleitems/song.html',
                           session=session,
                           page=page,
                           user=user_details,
                           song=song,
                           songmetadata=songmetadata)


#####################################################
#   Query (6)
#   Individual Podcast
#####################################################
@app.route('/podcast/<podcast_id>')
def single_podcast(podcast_id):
    page['title'] = 'Podcast'

    podcast = None
    podcast = database.get_podcast(podcast_id)

    podcasteps = None
    podcasteps = database.get_all_podcasteps_for_podcast(podcast_id)

    # Data integrity checks
    if podcast == None:
        podcast = []

    if podcasteps == None:
        podcasteps = []

    return render_template('singleitems/podcast.html',
                           session=session,
                           page=page,
                           user=user_details,
                           podcast=podcast,
                           podcasteps=podcasteps)


#####################################################
#   Query (7)
#   Individual Podcast Episode
#####################################################
@app.route('/podcastep/<media_id>')
def single_podcastep(media_id):
    page['title'] = 'Podcast Episode'

    podcastep = None
    podcastep = database.get_podcastep(media_id)

    if podcastep == None:
        podcastep = []

    return render_template('singleitems/podcastep.html',
                           session=session,
                           page=page,
                           user=user_details,
                           podcastep=podcastep)


#####################################################
#   Individual Movie
#####################################################
@app.route('/movie/<movie_id>')
def single_movie(movie_id):
    """
    Show a single movie by movie_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Movies'

    # Get a list of all movies by movie_id from the database
    movie = None
    movie = database.get_movie(movie_id)

    # Data integrity checks
    if movie == None:
        movie = []

    return render_template('singleitems/movie.html',
                           session=session,
                           page=page,
                           user=user_details,
                           movie=movie)


#####################################################
#   Individual Album
#####################################################
@app.route('/album/<album_id>')
def single_album(album_id):
    """
    Show a single album by album_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Albums'

    # Get the album plus associated metadata from the database
    album = None
    album = database.get_album(album_id)

    album_songs = None
    album_songs = database.get_album_songs(album_id)

    album_genres = None
    album_genres = database.get_album_genres(album_id)

    # Data integrity checks
    if album_songs == None:
        album_songs = []

    if album == None:
        album = []

    if album_genres == None:
        album_genres = []

    return render_template('singleitems/album.html',
                           session=session,
                           page=page,
                           user=user_details,
                           album=album,
                           album_songs=album_songs,
                           album_genres=album_genres)


#####################################################
#   Individual TVShow
#####################################################
@app.route('/tvshow/<tvshow_id>')
def single_tvshow(tvshow_id):
    """
    Show a single tvshows and its eps in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'TV Show'

    # Get a list of all tvshows by tvshow_id from the database
    tvshow = None
    tvshow = database.get_tvshow(tvshow_id)

    tvshoweps = None
    tvshoweps = database.get_all_tvshoweps_for_tvshow(tvshow_id)

    # Data integrity checks
    if tvshow == None:
        tvshow = []

    if tvshoweps == None:
        tvshoweps = []

    return render_template('singleitems/tvshow.html',
                           session=session,
                           page=page,
                           user=user_details,
                           tvshow=tvshow,
                           tvshoweps=tvshoweps)


#####################################################
#   Individual TVShow Episode
#####################################################
@app.route('/tvshowep/<tvshowep_id>')
def single_tvshowep(tvshowep_id):
    """
    Show a single tvshow episode in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List TV Shows'

    # Get a list of all tvshow eps by media_id from the database
    tvshowep = None
    tvshowep = database.get_tvshowep(tvshowep_id)

    # Data integrity checks
    if tvshowep == None:
        tvshowep = []

    return render_template('singleitems/tvshowep.html',
                           session=session,
                           page=page,
                           user=user_details,
                           tvshowep=tvshowep)


#####################################################
#   Query (10)
#   Individual Genre
#####################################################
@app.route('/genre/<type>/<genre_id>')
def single_genre(type, genre_id):

    page['title'] = 'Genre'  # Add the title
    genreitems = None
    if type == "film genre":
        type = "film"
        genreitems = database.get_genre_movies_and_shows(genre_id)
    elif type == "podcast genre":
        type = "podcast"
        genreitems = database.get_genre_podcasts(genre_id)
    elif type == "song genre":
        type = "song"
        genreitems = database.get_genre_songs(genre_id)

    if genreitems is None:
        genreitems = []
    return render_template('singleitems/genre.html',
                           session=session,
                           page=page,
                           user=user_details,
                           type=type,
                           genreitems=genreitems,
                           genreid=genre_id)


#####################################################
#####################################################
####    Search Items
#####################################################
#####################################################

#####################################################
#   Search TVShow
#####################################################
@app.route('/search/tvshow', methods=['POST', 'GET'])
def search_tvshows():
    """
    Search all the tvshows in your media server
    """

    # Check if the user is logged in, if not: back to login.
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'TV Show Search'

    # Get a list of matching tv shows from the database
    tvshows = None
    if (request.method == 'POST'):
        tvshows = database.find_matchingtvshows(request.form['searchterm'])

    # Data integrity checks
    if tvshows == None or tvshows == []:
        tvshows = []
        page['bar'] = False
        flash("No matching tv shows found, please try again")
    else:
        page['bar'] = True
        flash('Found ' + str(len(tvshows)) + ' results!')
        session['logged_in'] = True

    return render_template('searchitems/search_tvshows.html',
                           session=session,
                           page=page,
                           user=user_details,
                           tvshows=tvshows)


#####################################################
#   Query (9)
#   Search Movie
#####################################################
@app.route('/search/movie', methods=['POST', 'GET'])
def search_movies():
    # Check if the user is logged in, if not: back to login.
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    page['title'] = 'Movie Search'  # Add the title

    # Get a list of matching tv shows from the database
    movies = None
    if request.method == 'POST':
        movies = database.find_matchingmovies(request.form['searchterm'])

    # Data integrity checks
    if movies is None or movies == []:
        movies = []
        page['bar'] = False
        flash("No matching movies found, please try again")
    else:
        page['bar'] = True
        flash('Found ' + str(len(movies)) + ' results!')
        session['logged_in'] = True

    return render_template('searchitems/search_movies.html',
                           session=session,
                           page=page,
                           user=user_details,
                           movies=movies)


@app.route('/search/song', methods=['POST', 'GET'])
def search_songs():
    """
    Search all the movies in your media server
    """
    # Check if the user is logged in, if not: back to login.
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    page['title'] = 'Song Search'

    songs = None
    if request.method == 'POST':
        songs = database.find_matchingsongs(request.form['searchterm'])

    if songs is None or songs == []:
        page['bar'] = False
        flash("No matching songs found, please try again")
    else:
        page['bar'] = True
        flash('Found ' + str(len(songs)) + ' results!')
        session['logged_in'] = True

    return render_template('searchitems/search_songs.html',
                           session=session,
                           page=page,
                           user=user_details,
                           songs=songs)


@app.route('/search/artist', methods=['POST', 'GET'])
def search_artists():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    page['title'] = 'Artist Search'

    artists = None
    if request.method == 'POST':
        artists = database.find_matchingartists(request.form['searchterm'])

    if artists is None or artists == []:
        page['bar'] = False
        flash("No matching songs found, please try again")
    else:
        page['bar'] = True
        flash('Found ' + str(len(artists)) + ' results!')
        session['logged_in'] = True

    return render_template('searchitems/search_artists.html',
                           session=session,
                           page=page,
                           user=user_details,
                           artists=artists)


@app.route('/search/albums', methods=['POST', 'GET'])
def search_albums():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    page['title'] = 'Album Search'

    albums = None
    if request.method == 'POST':
        albums = database.find_matchingalbums(request.form['searchterm'])

    if albums is None or albums == []:
        page['bar'] = False
        flash("No matching songs found, please try again")
    else:
        page['bar'] = True
        flash('Found ' + str(len(albums)) + ' results!')
        session['logged_in'] = True

    return render_template('searchitems/search_albums.html',
                           session=session,
                           page=page,
                           user=user_details,
                           albums=albums)


@app.route('/search/podcasts', methods=['POST', 'GET'])
def search_podcasts():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    page['title'] = 'Podcast Search'

    podcasts = None
    if request.method == 'POST':
        podcasts = database.find_matchingpodcasts(request.form['searchterm'])

    if podcasts is None or podcasts == []:
        page['bar'] = False
        flash("No matching songs found, please try again")
    else:
        page['bar'] = True
        flash('Found ' + str(len(podcasts)) + ' results!')
        session['logged_in'] = True

    return render_template('searchitems/search_podcasts.html',
                           session=session,
                           page=page,
                           user=user_details,
                           podcasts=podcasts)


#####################################################
#   Add Movie
#####################################################
@app.route('/add/movie', methods=['POST', 'GET'])
def add_movie():
    """
    Add a new movie
    """
    # # Check if the user is logged in, if not: back to login.
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'Movie Creation'

    movies = None
    print("request form is:")
    newdict = {}
    print(request.form)

    # Check your incoming parameters
    if (request.method == 'POST'):

        # verify that the values are available:
        if ('movie_title' not in request.form):
            newdict['movie_title'] = 'Empty Film Value'
        else:
            newdict['movie_title'] = request.form['movie_title']
            print("We have a value: ", newdict['movie_title'])

        if ('release_year' not in request.form):
            newdict['release_year'] = '0'
        else:
            newdict['release_year'] = request.form['release_year']
            print("We have a value: ", newdict['release_year'])

        if ('description' not in request.form):
            newdict['description'] = 'Empty description field'
        else:
            newdict['description'] = request.form['description']
            print("We have a value: ", newdict['description'])

        if ('storage_location' not in request.form):
            newdict['storage_location'] = 'Empty storage location'
        else:
            newdict['storage_location'] = request.form['storage_location']
            print("We have a value: ", newdict['storage_location'])

        if ('film_genre' not in request.form):
            newdict['film_genre'] = 'drama'
        else:
            newdict['film_genre'] = request.form['film_genre']
            print("We have a value: ", newdict['film_genre'])

        if ('artwork' not in request.form):
            newdict[
                'artwork'] = 'https://user-images.githubusercontent.com/24848110/33519396-7e56363c-d79d-11e7-969b-09782f5ccbab.png'
        else:
            newdict['artwork'] = request.form['artwork']
            print("We have a value: ", newdict['artwork'])

        print('newdict is:')
        print(newdict)

        # forward to the database to manage insert
        movies = database.add_movie_to_db(newdict['movie_title'], newdict['release_year'], newdict['description'],
                                          newdict['storage_location'], newdict['film_genre'])

        max_movie_id = database.get_last_movie()[0]['movie_id']
        print(movies)
        if movies is not None:
            max_movie_id = movies[0]

        # ideally this would redirect to your newly added movie
        return single_movie(max_movie_id)
    else:
        return render_template('createitems/createmovie.html',
                               session=session,
                               page=page,
                               user=user_details)


#####################################################
#   Query (8)
#   Add song
#####################################################
@app.route('/add/song', methods=['POST', 'GET'])
def add_song():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    newdict = {}
    print(request.form)

    page['title'] = 'Song Creation'  # Add the title
    if request.method == 'POST':
        # location, songdescription, title, songlength, songgenre, artistid
        if 'title' not in request.form:
            newdict['title'] = ''
        else:
            newdict['title'] = request.form['title']
            print("We have a value: ", newdict['title'])

        if 'songdesc' not in request.form:
            newdict['description'] = ''
        else:
            newdict['description'] = request.form['songdesc']
            print("We have a value: ", newdict['description'])

        if 'location' not in request.form:
            newdict['location'] = ''
        else:
            newdict['location'] = request.form['location']
            print("We have a value: ", newdict['location'])

        if 'length' not in request.form:
            newdict['length'] = ''
        else:
            newdict['length'] = request.form['length']
            print("We have a value: ", newdict['length'])

        if 'genre' not in request.form:
            newdict['genre'] = ''
        else:
            newdict['genre'] = request.form['genre']
            print("We have a value: ", newdict['genre'])

        if 'artistid' not in request.form:
            newdict['artistid'] = ''
        else:
            newdict['artistid'] = request.form['artistid']
            print("We have a value: ", newdict['artistid'])

        print('songdict is:')
        print(newdict)
        id_artist = newdict['artistid']
        if id_artist.isdigit():
            pass
        else:
            page['bar'] = False
            flash("Artist ID must be an integer.")
            return render_template('createitems/createsong.html',
                                   session=session,
                                   page=page,
                                   user=user_details)
        a = database.check_artist(id_artist)

        if newdict['title'] == "":
            page['bar'] = False
            flash("Song requires a title.")
            return render_template('createitems/createsong.html',
                                   session=session,
                                   page=page,
                                   user=user_details)
        elif newdict['location'] == "":
            page['bar'] = False
            flash("Song requires a storage location.")
            return render_template('createitems/createsong.html',
                                   session=session,
                                   page=page,
                                   user=user_details)

        elif a != 1:
            page['bar'] = False
            flash("Artist does not exist.")
            return render_template('createitems/createsong.html',
                                   session=session,
                                   page=page,
                                   user=user_details)

        elif newdict['length'].isdigit() and newdict['artistid'].isdigit() and int(newdict['length']) > 0:
            songs = database.add_song_to_db(newdict['title'], newdict['description'], newdict['location'],
                                            newdict['length'], newdict['genre'], newdict['artistid'])

            return single_song(songs[0])
        else:
            page['bar'] = False
            flash("Invalid length or artist ID parameters.")
            return render_template('createitems/createsong.html',
                                   session=session,
                                   page=page,
                                   user=user_details)

    else:
        return render_template('createitems/createsong.html',
                               session=session,
                               page=page,
                               user=user_details)


@app.route('/account', methods=['POST', 'GET'])
def account():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    if request.method == 'POST':
        print("form: ")
        print(request.form)
        if "delete" in request.form:
            type = request.form['delete']
            code = database.delete_contact(type, user_details['username'])

            if code == 1:
                page['bar'] = True
                flash('You have successfully deleted your contact details.')
                global contact_details
                contact_details = database.get_contact_details(user_details['username'])
                print(user_details)
                print("user details ^")
                print(contact_details)
                print("contact  ^")
                return redirect(url_for('account'))

            else:
                page['bar'] = False
                flash('Error deleting contact details.')
                return redirect(url_for('account'))

        value = request.form['value']
        type = request.form['type']

        if type == "phone" and not value.isdigit():
            page['bar'] = False
            flash('Invalid phone number.')
            return redirect(url_for('account'))

        if type == "pass":
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512((value + salt).encode()).hexdigest()
            print("got here")
            code = database.change_password(hashed_password, salt, user_details['username'])

        else:
            code = database.change_contact(value, type, user_details['username'])

        if code == 1:
            page['bar'] = True
            flash('You have successfully changed your details')
            if type == "pass":
                user_details['password'] = value
                print(user_details)
                print("user details ^")
                return redirect(url_for('account'))

            contact_details = database.get_contact_details(user_details['username'])
            print(user_details)
            print("user details ^")
            print(contact_details)
            print("contact  ^")
            return redirect(url_for('account'))

        else:
            page['bar'] = False
            flash('Error changing details.')
            return redirect(url_for('account'))

    elif request.method == 'GET':
        print(user_details)
        print("user details ^")
        print("contact details:")
        contact_details = database.get_contact_details(user_details['username'])
        return (render_template('account.html',
                                session=session,
                                page=page,
                                user=user_details,
                                contact=contact_details))
