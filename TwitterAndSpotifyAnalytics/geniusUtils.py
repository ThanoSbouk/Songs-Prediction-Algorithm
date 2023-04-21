import lyricsgenius
import spotipy
from spotipy import SpotifyClientCredentials


#DISCLAIMER
#IN THIS STAGE, WE USE GENIUSUTILS.PY SCRIPT AS OUR TESTER !!!



genius = lyricsgenius.Genius('dJKEnMMk4-eEEBfVPGVf0HxDvWC4PNeK2IH75r2L0YgnxiEBAdm4t6NE2at8xayv')  # AccessToken
# artist = genius.search_artist("Drake", max_songs=5, sort="popularity")
# tracks = artist.songs
# print(artist.songs)
# for i in range(5):
#     print(tracks[i].lyrics)
#     print("---------------------------------")

if __name__ == "__main__":
    genius = lyricsgenius.Genius(
        'dJKEnMMk4-eEEBfVPGVf0HxDvWC4PNeK2IH75r2L0YgnxiEBAdm4t6NE2at8xayv')  # Genius AccessToken
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials("57e2e871e3524493b35ed78cc1661bd7",
                                                                                  "8ee934b00bde4dbe8aa649c9c9c1e77f"))  # spotify client id and secret

    song = spotify.track('https://open.spotify.com/track/2XU0oxnq2qxCpomAAuJY8K?si=478d6c794c764e41')
    fts = spotify.audio_features('https://open.spotify.com/track/2XU0oxnq2qxCpomAAuJY8K?si=478d6c794c764e41')
    song_name = song['name']
    allartists = []
    uris = []
    for artist in song['artists']:
        allartists.append(artist['name'])
    # id = ""
    # id = ['artists'][0]['uri']
    # followers = spotify.artist(['artists'][0]['uri'])
    # artist = spotify.artist('spotify:artist:2NjfBq1NflQcKSeiDooVjY')
    followers = spotify.artist(song['artists'][0]['uri'])['followers']['total']
    # followers = spotify.artist('spotify:artist:2NjfBq1NflQcKSeiDooVjY')['followers']['total']


    song_popularity = song['popularity']

    # energy= (fts[0]['energy'])
    # danceability= (fts[0]['danceability'])
    speechiness = (fts[0]['speechiness'])

    print(song_name)
    print(allartists)
    print(song_popularity)
    # print(fts)
    # print(energy)
    print(speechiness)

    # gartist = genius.search_artist("Drake",max_songs=3)
    # genius.excluded_terms = ["(Remix)", "(Live)", "(Chicago)"]  # Exclude songs with these words in their title
    # genius.skip_non_songs = False  # Include hits thought to be non-songs
    # lyrics = genius.search_song(title=song_name, artist=allartists).lyrics
    #
    # print(lyrics)

    print("Debugging Message")
