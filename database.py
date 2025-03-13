#!/usr/bin/env python3
"""
MediaServer Database module.
Contains all interactions between the webapp and the queries to the database.
"""

import configparser
import json
import sys
import hashlib
from modules import pg8000


################################################################################
#   Welcome to the database file, where all the query magic happens.
#   My biggest tip is look at the *week 8 lab*.
#   Important information:
#       - If you're getting issues and getting locked out of your database.
#           You may have reached the maximum number of connections.
#           Why? (You're not closing things!) Be careful!
#       - Check things *carefully*.
#       - There may be better ways to do things, this is just for example
#           purposes
#       - ORDERING MATTERS
#           - Unfortunately to make it easier for everyone, we have to ask that
#               your columns are in order. WATCH YOUR SELECTS!! :)
#   Good luck!
#       And remember to have some fun :D
################################################################################

#############################
#                           #
# Database Helper Functions #
#                           #
#############################


#####################################################
#   Database Connect
#   (No need to touch
#       (unless the exception is potatoing))
#####################################################

def database_connect():
    """
    Connects to the database using the connection string.
    If 'None' was returned it means there was an issue connecting to
    the database. It would be wise to handle this ;)
    """
    # Read the config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'database' not in config['DATABASE']:
        config['DATABASE']['database'] = config['DATABASE']['user']

    # Create a connection to the database
    connection = None
    try:
        # Parses the config file and connects using the connect string
        connection = pg8000.connect(database=config['DATABASE']['database'],
                                    user=config['DATABASE']['user'],
                                    password=config['DATABASE']['password'],
                                    host=config['DATABASE']['host'])
    except pg8000.OperationalError as operation_error:
        print("""Error, you haven't updated your config.ini or you have a bad
        connection, please try again. (Update your files first, then check
        internet connection)
        """)
        print(operation_error)
        return None

    # return the connection to use
    return connection


##################################################
# Print a SQL string to see how it would insert  #
##################################################

def print_sql_string(inputstring, params=None):
    """
    Prints out a string as a SQL string parameterized assuming all strings
    """

    if params is not None:
        if params != []:
            inputstring = inputstring.replace("%s", "'%s'")

    print(inputstring % params)


#####################################################
#   SQL Dictionary Fetch
#   useful for pulling particular items as a dict
#   (No need to touch
#       (unless the exception is potatoing))
#   Expected return:
#       singlerow:  [{col1name:col1value,col2name:col2value, etc.}]
#       multiplerow: [{col1name:col1value,col2name:col2value, etc.},
#           {col1name:col1value,col2name:col2value, etc.},
#           etc.]
#####################################################

def dictfetchall(cursor, sqltext, params=None):
    """ Returns query results as list of dictionaries."""

    result = []
    if (params is None):
        print(sqltext)
    else:
        print("we HAVE PARAMS!")
        print_sql_string(sqltext, params)

    cursor.execute(sqltext, params)
    cols = [a[0].decode("utf-8") for a in cursor.description]
    print(cols)
    returnres = cursor.fetchall()
    for row in returnres:
        result.append({a: b for a, b in zip(cols, row)})
    # cursor.close()
    return result


def dictfetchone(cursor, sqltext, params=None):
    """ Returns query results as list of dictionaries."""
    # cursor = conn.cursor()
    result = []
    cursor.execute(sqltext, params)
    cols = [a[0].decode("utf-8") for a in cursor.description]
    returnres = cursor.fetchone()
    result.append({a: b for a, b in zip(cols, returnres)})
    return result


#####################################################
#   Query (1)
#   Login
#####################################################
def check_login_unsafe(username, password):
    """
    Check that the users information exists in the database.
        - True => return the user data
        - False => return None
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #############################################################################
        # Fill in the SQL below in a manner similar to Wk 08 Lab to log the user in #
        #############################################################################

        sql = """SELECT *
        FROM mediaserver.useraccount
        WHERE username=%s AND password=%s;"""

        print(username)
        print(password)

        r = dictfetchone(cur, sql, (username, password))
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Error Invalid Login")
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


def check_login(username, password, salt):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below in a manner similar to Wk 08 Lab to log the user in #
        #############################################################################
        hashed_password = hashlib.sha512((password + salt).encode()).hexdigest()

        sql = """SELECT *
                FROM mediaserver.useraccount
                WHERE username=%s AND password=%s;"""
        r = dictfetchone(cur, sql, (username, hashed_password))

        cur.close()
        conn.close()
        return r
    except Exception:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Error Invalid Login")
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Is Superuser? -
#   is this required? we can get this from the login information
#####################################################

def is_superuser(username):
    """
    Check if the user is a superuser.
        - True => Get the departments as a list.
        - False => Return None
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """SELECT isSuper
                 FROM mediaserver.useraccount
                 WHERE username=%s AND isSuper"""
        print("username is: " + username)
        cur.execute(sql, (username))
        r = cur.fetchone()  # Fetch the first row
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (1 b)
#   Get user playlists
#####################################################
def user_playlists(username):
    """
    Check if user has any playlists
        - True -> Return all user playlists
        - False -> Return None
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        ###############################################################################
        # Fill in the SQL below and make sure you get all the playlists for this user #
        ###############################################################################
        sql = """SELECT collection_id, collection_name, COUNT(media_id)
                 FROM mediaserver.mediacollection NATURAL JOIN mediaserver.mediacollectioncontents
                 WHERE username=%s
                 GROUP BY collection_id, collection_name;"""

        print("username is: " + username)
        r = dictfetchall(cur, sql, (username,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting User Playlists:", sys.exc_info()[0])
        raise


#####################################################
#   Query (1 a)
#   Get user podcasts
#####################################################
def user_podcast_subscriptions(username):
    """
    Get user podcast subscriptions.
    """

    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #################################################################################
        # Fill in the SQL below and get all the podcasts that the user is subscribed to #
        #################################################################################

        sql = """SELECT podcast_id, podcast_title, podcast_uri, podcast_last_updated
                 FROM mediaserver.podcast NATURAL JOIN mediaserver.subscribed_podcasts
                 WHERE username=%s;"""

        r = dictfetchall(cur, sql, (username,))
        print("return val is:")
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcast subs:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (1 c)
#   Get user in progress items
#####################################################
def user_in_progress_items(username):
    """
    Get user in progress items that aren't 100%
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        ###################################################################################
        # Fill in the SQL below with a way to find all the in progress items for the user #
        ###################################################################################

        sql = """SELECT media_id, play_count, progress, lastviewed, storage_location
                 FROM  mediaserver.usermediaconsumption NATURAL JOIN mediaserver.mediaitem
                 WHERE username=%s AND progress < 100
                 ORDER BY lastviewed DESC;"""

        r = dictfetchall(cur, sql, (username,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting User Consumption - Likely no values:", sys.exc_info()[0])
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get all artists
#####################################################
def get_allartists():
    """
    Get all the artists in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select
            a.artist_id, a.artist_name, count(amd.md_id) as count
        from
            mediaserver.artist a left outer join mediaserver.artistmetadata amd on (a.artist_id=amd.artist_id)
        group by a.artist_id, a.artist_name
        order by a.artist_name;"""

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Artists:", sys.exc_info()[0])
        raise

#####################################################
#   Get all songs
#####################################################
def get_allsongs():
    """
    Get all the songs in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select
            s.song_id, s.song_title, string_agg(saa.artist_name,',') as artists
        from
            mediaserver.song s left outer join
            (mediaserver.Song_Artists sa join mediaserver.Artist a on (sa.performing_artist_id=a.artist_id)
            ) as saa  on (s.song_id=saa.song_id)
        group by s.song_id, s.song_title
        order by s.song_id"""

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Songs:", sys.exc_info()[0])
        raise

#####################################################
#   Get all podcasts
#####################################################
def get_allpodcasts():
    """
    Get all the podcasts in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select
                p.*, pnew.count as count
            from
                mediaserver.podcast p,
                (select
                    p1.podcast_id, count(*) as count
                from
                    mediaserver.podcast p1 left outer join mediaserver.podcastepisode pe1 on (p1.podcast_id=pe1.podcast_id)
                    group by p1.podcast_id) pnew
            where p.podcast_id = pnew.podcast_id;"""

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Podcasts:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get all albums
#####################################################
def get_allalbums():
    """
    Get all the Albums in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select
                a.album_id, a.album_title, anew.count as count, anew.artists
            from
                mediaserver.album a,
                (select
                    a1.album_id, count(distinct as1.song_id) as count, array_to_string(array_agg(distinct ar1.artist_name),', ') as artists
                from
                    mediaserver.album a1
			left outer join mediaserver.album_songs as1 on (a1.album_id=as1.album_id)
			left outer join mediaserver.song s1 on (as1.song_id=s1.song_id)
			left outer join mediaserver.Song_Artists sa1 on (s1.song_id=sa1.song_id)
			left outer join mediaserver.artist ar1 on (sa1.performing_artist_id=ar1.artist_id)
                group by a1.album_id) anew
            where a.album_id = anew.album_id;"""

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Albums:", sys.exc_info()[0])
        raise

#####################################################
#   Query (3 a,b c)
#   Get all tvshows
#####################################################
def get_alltvshows():
    """
    Get all the TV Shows in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all tv shows and episode counts #
        #############################################################################
        sql = """
        SELECT tvshow_id, tvshow_title, COUNT(episode) FROM mediaserver.tvepisode INNER JOIN mediaserver.tvshow USING (tvshow_id)
            GROUP BY tvshow_id, tvshow_title
            ORDER BY tvshow_id;
        """

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise

#####################################################
#   Get all movies
#####################################################
def get_allmovies():
    """
    Get all the Movies in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select
            m.movie_id, m.movie_title, m.release_year, count(mimd.md_id) as count
        from
            mediaserver.movie m left outer join mediaserver.mediaitemmetadata mimd on (m.movie_id = mimd.media_id)
        group by m.movie_id, m.movie_title, m.release_year
        order by movie_id;"""

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Movies:", sys.exc_info()[0])
        raise

#####################################################
#   Get one artist
#####################################################
def get_artist(artist_id):
    """
    Get an artist by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select *
        from mediaserver.artist a left outer join
            (mediaserver.artistmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) amd
        on (a.artist_id=amd.artist_id)
        where a.artist_id=%s"""

        r = dictfetchall(cur, sql, (artist_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Artist with ID: '" + artist_id + "'", sys.exc_info()[0])
        raise


#####################################################
#   Query (2 a,b,c)
#   Get one song
#####################################################
def get_song(song_id):
    """
    Get a song by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a song    #
        # and the artists that performed it                                         #
        #############################################################################
        sql = """
        SELECT song_title, STRING_AGG(artist_name, ', ') AS artists, length
            FROM mediaserver.song FULL OUTER JOIN mediaserver.song_artists USING (song_id)
            INNER JOIN mediaserver.artist ON (song_artists.performing_artist_id = artist.artist_id)
            WHERE song_id=%s
            GROUP BY song_title, length;
        """

        r = dictfetchall(cur, sql, (song_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Songs:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (2 d)
#   Get metadata for one song
#####################################################
def get_song_metadata(song_id):
    """
    Get the meta for a song by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all metadata about a song       #
        #############################################################################

        sql = """
        SELECT md_type_name, STRING_AGG(md_value, ', ') AS md_value FROM mediaserver.mediaitemmetadata
            FULL OUTER JOIN mediaserver.metadata USING (md_id)
            INNER JOIN mediaserver.metadatatype USING (md_type_id)
            WHERE media_id=%s
            GROUP BY md_type_name
        UNION
        SELECT md_type_name, md_value FROM mediaserver.song
            INNER JOIN mediaserver.album_songs USING (song_id)
            INNER JOIN mediaserver.albummetadata USING (album_id)
            INNER JOIN mediaserver.metadata USING (md_id)
            INNER JOIN mediaserver.metadatatype USING (md_type_id)
            WHERE song_id=%s
        UNION
        SELECT md_type_name, md_value FROM mediaserver.song_artists
            JOIN mediaserver.artistmetadata ON (song_artists.performing_artist_id = artistmetadata.artist_id)
            INNER JOIN mediaserver.metadata USING (md_id)
            INNER JOIN mediaserver.metadatatype USING (md_type_id)
            WHERE song_id=%s;
        """

        r = dictfetchall(cur, sql, (song_id, song_id, song_id))
        for dict in r:
            if dict['md_type_name'] == "song genre":
                for genre in dict['md_value'].split(","):
                    string = genre.strip()
                    newdict = {'md_type_name': 'song genre',
                               'md_value': string}
                    r.append(newdict)
                r.remove(dict)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting song metadata for ID: " + song_id, sys.exc_info()[0])
        raise

#####################################################
#   Query (6 a,b,c,d,e)
#   Get one podcast and return all metadata associated with it
#####################################################
def get_podcast(podcast_id):
    """
    Get a podcast by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a podcast #
        # including all metadata associated with it                                 #
        #############################################################################
        sql = """SELECT podcast_id, podcast_title, podcast_uri, podcast_last_updated, md_type_name, md_value
        FROM mediaserver.podcast INNER JOIN mediaserver.podcastmetadata USING (podcast_id)
        INNER JOIN mediaserver.metadata USING (md_id)
        INNER JOIN mediaserver.metadatatype USING (md_type_id)
        WHERE podcast_id=%s;
        """

        r = dictfetchall(cur, sql, (podcast_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcast with ID: " + podcast_id, sys.exc_info()[0])
        raise

####################################################
#   Query (6 f)
#   Get all podcast eps for one podcast
#####################################################
def get_all_podcasteps_for_podcast(podcast_id):
    """
    Get all podcast eps for one podcast by their podcast ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # podcast episodes in a podcast                                             #
        #############################################################################

        sql = """SELECT media_id, podcast_episode_title, podcast_episode_uri, podcast_episode_published_date, podcast_episode_length
        FROM mediaserver.podcastepisode
        WHERE podcast_id=%s
        ORDER BY podcast_episode_published_date DESC;"""

        r = dictfetchall(cur, sql, (podcast_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Podcast Episodes for Podcast with ID: " + podcast_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (7 a,b,c,d,e,f)
#   Get one podcast ep and associated metadata
#####################################################
def get_podcastep(podcastep_id):
    """
    Get a podcast ep by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a         #
        # podcast episodes and it's associated metadata                             #
        #############################################################################
        sql = """SELECT media_id, podcast_episode_title, podcast_episode_uri,
                         podcast_episode_published_date, podcast_episode_length, md_type_name, md_value
                         FROM mediaserver.podcastepisode
                         INNER JOIN mediaserver.mediaitemmetadata USING (media_id)
                         INNER JOIN mediaserver.metadata USING (md_id)
                         INNER JOIN mediaserver.metadatatype USING (md_type_id)
                         WHERE media_id=%s;"""

        r = dictfetchall(cur, sql, (podcastep_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcast Episode with ID: " + podcastep_id, sys.exc_info()[0])
        raise


#####################################################
#   Query (5 a,b)
#   Get one album
#####################################################
def get_album(album_id):
    """
    Get an album by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about an album  #
        # including all relevant metadata                                           #
        #############################################################################
        sql = """SELECT album_title, md_value, md_type_name
                 FROM mediaserver.album NATURAL JOIN mediaserver.albummetadata NATURAL JOIN mediaserver.metadata NATURAL JOIN mediaserver.metadatatype
                 WHERE album_id=%s;"""

        r = dictfetchall(cur, sql, (album_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Albums with ID: " + album_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (5 d)
#   Get all songs for one album
#####################################################
def get_album_songs(album_id):
    """
    Get all songs for an album by the album ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # songs in an album, including their artists                                #
        #############################################################################
        sql = """SELECT song_id, song_title, STRING_AGG(artist_name, ', ') AS artists
                 FROM mediaserver.album_songs NATURAL JOIN mediaserver.song NATURAL JOIN mediaserver.song_artists NATURAL JOIN mediaserver.artist
                 WHERE album_id=%s AND performing_artist_id = artist_id
                 GROUP BY song_id, song_title, track_num
                 ORDER BY track_num ASC;"""

        r = dictfetchall(cur, sql, (album_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Albums songs with ID: " + album_id, sys.exc_info()[0])
        raise

#####################################################
#   Query (5 c)
#   Get all genres for one album
#####################################################
def get_album_genres(album_id):
    """
    Get all genres for an album by the album ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # genres in an album (based on all the genres of the songs in that album)   #
        #############################################################################
        sql = """SELECT md_type_name, STRING_AGG(DISTINCT(md_value), ', ') AS songgenres
                 FROM mediaserver.album_songs
                 INNER JOIN mediaserver.mediaitemmetadata ON (song_id = media_id)
                 INNER JOIN mediaserver.metadata USING (md_id)
                 INNER JOIN mediaserver.metadatatype USING (md_type_id)
                 WHERE album_id=%s
                 GROUP BY md_type_name;"""

        r = dictfetchall(cur, sql, (album_id,))

        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Albums genres with ID: " + album_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (10)
#   May require the addition of SQL to multiple
#   functions and the creation of a new function to
#   determine what type of genre is being provided
#   You may have to look at the hard coded values
#   in the sampledata to make your choices
#####################################################

#####################################################
#   Query (10)
#   Get all songs for one song_genre
#####################################################
def get_genre_songs(genre_id):
    """
    Get all songs for a particular song_genre ID in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # songs which belong to a particular genre_id                               #
        #############################################################################
        sql = """
        SELECT song_id AS id, song_title AS title, artist_name FROM mediaserver.metadata
        INNER JOIN mediaserver.metadatatype USING (md_type_id)
        INNER JOIN mediaserver.mediaitemmetadata USING (md_id)
        INNER JOIN mediaserver.song ON (song_id=media_id)
        INNER JOIN mediaserver.song_artists USING (song_id)
        INNER JOIN mediaserver.artist ON (performing_artist_id=artist_id)
        WHERE md_type_name = 'song genre'
        AND md_value = %s
        """

        r = dictfetchall(cur, sql, (genre_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Songs with Genre ID: " + genre_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (10)
#   Get all podcasts for one podcast_genre
#####################################################
def get_genre_podcasts(genre_id):
    """
    Get all podcasts for a particular podcast_genre ID in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # podcasts which belong to a particular genre_id                            #
        #############################################################################
        sql = """
        SELECT podcast_id AS id, podcast_title AS title, podcast_last_updated AS last_updated
        FROM mediaserver.podcast
        INNER JOIN mediaserver.podcastmetadata USING (podcast_id)
        INNER JOIN mediaserver.metadata USING (md_id)
        INNER JOIN mediaserver.metadatatype USING (md_type_id)
        WHERE md_type_name = 'podcast genre'
        AND md_value = %s
        """

        r = dictfetchall(cur, sql, (genre_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcasts with Genre ID: " + genre_id, sys.exc_info()[0])
        raise


#####################################################
#   Query (10)
#   Get all movies and tv shows for one film_genre
#####################################################
def get_genre_movies_and_shows(genre_id):
    """
    Get all movies and tv shows for a particular film_genre ID in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # movies and tv shows which belong to a particular genre_id                 #
        #############################################################################
        sql = """
        SELECT tvshow_id AS id, tvshow_title AS title, 'tvshow' AS type FROM mediaserver.metadata
        INNER JOIN mediaserver.metadatatype USING (md_type_id)
        INNER JOIN mediaserver.tvshowmetadata USING (md_id)
        INNER JOIN mediaserver.tvshow USING (tvshow_id)
        WHERE md_type_name = 'film genre'
        AND md_value = %s
        UNION
        SELECT movie_id AS id, movie_title AS title, 'movie' AS type FROM mediaserver.movie
        INNER JOIN mediaserver.mediaitemmetadata ON (movie_id=media_id)
        INNER JOIN mediaserver.metadata USING (md_id)
        INNER JOIN mediaserver.metadatatype USING (md_type_id)
        WHERE md_type_name = 'film genre'
        AND md_value = %s
        """

        r = dictfetchall(cur, sql, (genre_id, genre_id))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Movies and tv shows with Genre ID: " + genre_id, sys.exc_info()[0])
        raise


#####################################################
#   Query (4 a,b)
#   Get one tvshow
#####################################################
def get_tvshow(tvshow_id):
    """
    Get one tvshow in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a tv show #
        # including all relevant metadata       #
        #############################################################################
        sql = """
        SELECT md_type_name, STRING_AGG(md_value, ', ') as md_value
            FROM mediaserver.tvshowmetadata
            FULL OUTER JOIN mediaserver.tvshow USING (tvshow_id)
            INNER JOIN mediaserver.metadata USING (md_id)
            INNER JOIN mediaserver.metadatatype USING (md_type_id)
            WHERE tvshow.tvshow_id=%s
            GROUP BY tvshow_title, md_type_name
        """

        r = dictfetchall(cur, sql, (tvshow_id,))
        print("return val for tv_show is:")

        for dict in r:
            if (dict['md_type_name'] == "film genre"):
                for genre in dict['md_value'].split(","):
                    string = genre.strip()
                    newdict = {'md_type_name': 'film genre',
                               'md_value': string}
                    r.append(newdict)
                r.remove(dict)
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (4 c)
#   Get all tv show episodes for one tv show
#####################################################
def get_all_tvshoweps_for_tvshow(tvshow_id):
    """
    Get all tvshow episodes for one tv show in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # tv episodes in a tv show                                                  #
        #############################################################################
        sql = """
        SELECT media_id, tvshow_id, tvshow_episode_title, season, episode, air_date
            FROM mediaserver.tvepisode
            WHERE tvshow_id=%s
            ORDER BY season, episode;
        """

        r = dictfetchall(cur, sql, (tvshow_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get one tvshow episode
#####################################################
def get_tvshowep(tvshowep_id):
    """
    Get one tvshow episode in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select *
        from mediaserver.TVEpisode te left outer join
            (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) temd
            on (te.media_id=temd.media_id)
        where te.media_id = %s"""

        r = dictfetchall(cur, sql, (tvshowep_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################

#   Get one movie
#####################################################
def get_movie(movie_id):
    """
    Get one movie in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select *
        from mediaserver.movie m left outer join
            (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) mmd
        on (m.movie_id=mmd.media_id)
        where m.movie_id=%s;"""

        r = dictfetchall(cur, sql, (movie_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Movies:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Find all matching tvshows
#####################################################
def find_matchingtvshows(searchterm):
    """
    Get all the matching TV Shows in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
            select
                t.*, tnew.count as count
            from
                mediaserver.tvshow t,
                (select
                    t1.tvshow_id, count(te1.media_id) as count
                from
                    mediaserver.tvshow t1 left outer join mediaserver.TVEpisode te1 on (t1.tvshow_id=te1.tvshow_id)
                    group by t1.tvshow_id) tnew
            where t.tvshow_id = tnew.tvshow_id and lower(tvshow_title) ~ lower(%s)
            order by t.tvshow_id;"""

        r = dictfetchall(cur, sql, (searchterm,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise


#####################################################
#   Query (9)
#   Find all matching Movies
#####################################################
def find_matchingmovies(searchterm):
    """
    Get all the matching Movies in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about movies    #
        # that match a given search term                                            #
        #############################################################################
        sql = """
            SELECT *
                FROM mediaserver.movie
                WHERE LOWER(movie_title) LIKE CONCAT('%%', LOWER(%s), '%%')
                ORDER BY movie_id;
        """

        r = dictfetchall(cur, sql, (searchterm,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise


def find_matchingsongs(searchterm):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        #############################################################################
        sql = """
            SELECT song_id, song_title, STRING_AGG(artist_name, ', ') AS artists
            FROM mediaserver.song FULL OUTER JOIN mediaserver.song_artists USING (song_id)
            INNER JOIN mediaserver.artist ON (song_artists.performing_artist_id = artist.artist_id)
            WHERE LOWER(song_title) LIKE CONCAT('%%', LOWER(%s), '%%')
            GROUP BY song_id, song_title
            ORDER BY song_id;
            """

        r = dictfetchall(cur, sql, (searchterm,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except Exception:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise


def find_matchingartists(searchterm):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        #############################################################################
        sql = """
            SELECT *
            FROM mediaserver.artist
            WHERE LOWER(artist_name) LIKE CONCAT('%%', LOWER(%s), '%%')
            ORDER BY artist_id;
            """

        r = dictfetchall(cur, sql, (searchterm,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except Exception:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise


def find_matchingalbums(searchterm):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        #############################################################################
        sql = """
            SELECT album_id, album_title, COUNT(song_id) AS count
            FROM mediaserver.album
            INNER JOIN mediaserver.album_songs USING (album_id)
            WHERE LOWER(album_title) LIKE CONCAT('%%', LOWER(%s), '%%')
            GROUP BY album_id, album_title
            ORDER BY album_id ASC;
            """

        r = dictfetchall(cur, sql, (searchterm,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except Exception:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise


def find_matchingpodcasts(searchterm):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        #############################################################################
        sql = """
            SELECT podcast_id, podcast_title, COUNT(podcast_id) AS count
            FROM mediaserver.podcast
            INNER JOIN mediaserver.podcastepisode USING (podcast_id)
            WHERE LOWER(podcast_title) LIKE CONCAT('%%', LOWER(%s), '%%')
            GROUP BY podcast_id, podcast_title
            ORDER BY podcast_id ASC
            """

        r = dictfetchall(cur, sql, (searchterm,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except Exception:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise


#####################################################
#   Add a new Movie
#####################################################
def add_movie_to_db(title, release_year, description, storage_location, genre):
    """
    Add a new Movie to your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        SELECT
            mediaserver.addMovie(
                %s,%s,%s,%s,%s);
        """

        cur.execute(sql, (storage_location, description, title, release_year, genre))
        conn.commit()  # Commit the transaction
        r = cur.fetchone()
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a movie:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (8)
#   Add a new Song
#####################################################
def add_song_to_db(title, description, location, length, genre, artistid):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:

        # location, songdescription, title, songlength, songgenre, artistid
        sql = """
        SELECT
            mediaserver.addSong(
                %s,%s,%s,%s,%s,%s);
        """

        cur.execute(sql, (title, description, location, length, genre, artistid))
        conn.commit()  # Commit the transaction
        r = cur.fetchone()
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding song: ", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None
    #############################################################################
    # Fill in the Function  with a query and management for how to add a new    #
    # song to your media server. Make sure you manage all constraints           #
    #############################################################################


def check_artist(artist_id):
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select artist_id FROM
        mediaserver.artist
        WHERE artist_id=%s;
        """
        r = dictfetchall(cur, sql, (artist_id,))
        print("return val for artist check is:")
        print(r)
        if len(r) == 0:
            return 0
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return 1
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error checking artist: '" + artist_id + "'", sys.exc_info()[0])
        raise


def get_last_movie():
    """
    Get all the latest entered movie in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        select max(movie_id) as movie_id from mediaserver.movie"""

        r = dictfetchone(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a movie:", sys.exc_info()[0])
        raise

#  FOR MARKING PURPOSES ONLY
#  DO NOT CHANGE

def to_json(fn_name, ret_val):
    """
    TO_JSON used for marking; Gives the function name and the
    return value in JSON.
    """
    return {'function': fn_name, 'res': json.dumps(ret_val)}


# =================================================================
# =================================================================
def change_password(new, salt, user):
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        sql = """UPDATE mediaserver.useraccount
                SET password=%s,
                salt=%s
                WHERE username=%s
                RETURNING *;
                """

        cur.execute(sql, (new, salt, user))
        r = cur.fetchall()
        print("return:")
        print(r)
        if len(r) != 0:
            conn.commit()
            cur.close()  # Close the cursor
            conn.close()  # Close the connection to the db
            return 1
        else:
            cur.close()  # Close the cursor
            conn.close()  # Close the connection to the db
            return -1
    except Exception as e:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Error when changing password")
        print(e)

    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


def get_contact_details(username):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        sql = """
            SELECT contact_type_name, contact_type_value
            FROM mediaserver.contactmethod
            INNER JOIN mediaserver.contacttype USING (contact_type_id)
            WHERE username=%s
            """
        r = dictfetchall(cur, sql, (username,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Error getting contact details:")
        print(sys.exc_info()[0])
        raise


def change_contact(val, type, user):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        if type == "email":
            sql = """
                INSERT INTO mediaserver.contactmethod (username, contact_type_id, contact_type_value)
                VALUES(%s, 1, %s)
                ON CONFLICT (username, contact_type_id) DO UPDATE SET contact_type_value = %s
                WHERE contactmethod.username=%s AND contactmethod.contact_type_id=1
                RETURNING *;
                """
        elif type == "phone":
            sql = """
                INSERT INTO mediaserver.contactmethod (username, contact_type_id, contact_type_value)
                VALUES(%s, 2, %s)
                ON CONFLICT (username, contact_type_id) DO UPDATE SET contact_type_value = %s
                WHERE contactmethod.username=%s AND contactmethod.contact_type_id=2
                RETURNING *;
                """
        else:
            sql = """
                INSERT INTO mediaserver.contactmethod (username, contact_type_id, contact_type_value)
                VALUES(%s, 3, %s)
                ON CONFLICT (username, contact_type_id) DO UPDATE SET contact_type_value = %s
                WHERE contactmethod.username=%s AND contactmethod.contact_type_id=3
                RETURNING *;
                """
        cur.execute(sql, (user, val, val, user))
        r = cur.fetchall()
        print("return:")
        print(r)
        if len(r) != 0:
            conn.commit()
            cur.close()  # Close the cursor
            conn.close()  # Close the connection to the db
            return 1
        else:
            cur.close()  # Close the cursor
            conn.close()  # Close the connection to the db
            return -1
    except Exception as e:
        print("Error changing contact details")
        print(e)

    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


def delete_contact(type, user):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        if type == "email":
            sql = """
                DELETE FROM mediaserver.contactmethod
                WHERE contact_type_id=1 AND username=%s
                RETURNING *
                """
        elif type == "phone":
            sql = """
                DELETE FROM mediaserver.contactmethod
                WHERE contact_type_id=2 AND username=%s
                RETURNING *
                """
        else:
            sql = """
                DELETE FROM mediaserver.contactmethod
                WHERE contact_type_id=3 AND username=%s
                RETURNING *
                """
        print(type, user)
        cur.execute(sql, (user,))
        r = cur.fetchall()
        print("return:")
        print(r)
        if len(r) != 0:
            conn.commit()
            cur.close()  # Close the cursor
            conn.close()  # Close the connection to the db
            return 1
        else:
            cur.close()  # Close the cursor
            conn.close()  # Close the connection to the db
            return -1
    except Exception as e:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Error deleting contact details")
        print(e)
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


def get_salt(username):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        sql = """SELECT salt
        FROM mediaserver.useraccount
        WHERE username=%s;"""

        r = dictfetchone(cur, sql, (username,))
        print("salt dic ", r)
        return r
    except Exception:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Error Invalid Login")
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return None
