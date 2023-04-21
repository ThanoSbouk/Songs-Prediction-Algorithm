import spotipy
import json
import re
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import concatJSONFiles
from concatJSONFiles import concat_json_files , retrieveRetweetsFullText , retrieveSpotifyUrls

# birdy_uri ='spotify:artist:7dGJo4pcD2V6oG8kP0tJRR' #Eminem Spotify uri
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials("57e2e871e3524493b35ed78cc1661bd7",
                                                                              "8ee934b00bde4dbe8aa649c9c9c1e77f"))  # spotify client id and secret


# results = spotify.artist_albums(birdy_uri, album_type='album')
# albums = results['items']
# while results['next']:
#  results = spotify.next(results)
#  albums.extend(results['items'])

def getTrackinfo(spotifylinks):
    spotifyinfo = []
    # concatJSONFiles.retrieveSpotifyUrls()
    spotifylinks['song_title'] = ""
    spotifylinks['artist_name'] = ""
    spotifylinks['song_popularity'] = ""
    for index, row in spotifylinks.iterrows():
        try:
            if (len(row['spotify_urls']) != 0 and row['spotify_urls'][0] != -1):
              # spotifyinfo.append(spotify.track(row['spotify_urls'][0]))
                spotify_track_info = spotify.track(row['spotify_urls'][0])
                row['song_title'] = spotify_track_info['name']
                artistlist = []
                for artist in spotify_track_info['artists']:
                    artistlist.append(artist['name'])
                row['artist_name'] = artistlist
                row['song_popularity'] = spotify_track_info['popularity']
            else :
                row['song_title'] = [-1]
                row['artist_name'] = [-1]
                row['song_popularity'] = [-1]

        except Exception:
            print("ERROR")
            row['song_title'] = "Error 400"
            row['artist_name'] = "Error 400"
            row['song_popularity'] = "Error 400"
            # print('Could not process link ' + row['spotify_urls'])

    return spotifylinks
    # here we have to make a for loop , passing all the links to the spotify.track command in the line below
    # count = 0
    # for i in range(len(spotifylinks) - 1):
    #     try:
    #         spotifyinfo.append(spotify.track(spotifylinks[i]))
    #         track = spotifyinfo[i]
    #         # if (spotifyinfo.popularity[i] > 60):
    #         #     print(spotifyinfo[i].name)
    #         #     for artist in track['artists']:
    #         #         print(artist['name'])
    #     except Exception:
    #         print('Could not process link ' + spotifylinks[i]);
    #         count = count + 1
    #
    # print('skipped ' + count + 'songs')


# print("Debugging Message")


# print(json.dumps(song,indent=4, sort_keys=True))


# for album in albums:
# print(album['name'])


