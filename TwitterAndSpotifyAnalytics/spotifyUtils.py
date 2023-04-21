import spotipy
import re
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import pickle

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials("57e2e871e3524493b35ed78cc1661bd7",
                                                                              "8ee934b00bde4dbe8aa649c9c9c1e77f"))  # spotify client id and secret
# path = r'../../Desktop/ceid/Thesis/Top 100 Billboard 2020 - Sheet1.csv'
# with open(path) as csvfile:
#     df = pd.read_csv(csvfile, header=0, usecols=['Rank', 'Spotify Link'])

# #Pickle Files
# audio_dict = df
# filename = 'Audio Features'
# outfile = open(filename,'wb')
# pickle.dump(audio_dict,outfile)
# outfile.close()
#
# #Unpickle Files
# infile = open(filename,'rb')
# new_dict = pickle.load(infile)
# infile.close()

df= pd.read_pickle('./Audio Features All')

def retrieveSpotifyUrls(df):
    entities_list = list(df["entities"].to_dict().values())

    spotify_urls = []
    for idx, d in enumerate(entities_list):
        if not pd.isna(d) and 'urls' in d:  # pd.isna(d) is needed due to truncated retweets
            tweetsUrls = []
            for url in d['urls']:
                if "open.spotify.com/track" in url['Spotify Link']:
                    tweetsUrls.append(re.sub(r'\?\S*', '', url['Spotify Link']))
            spotify_urls.append(tweetsUrls)
        else:
            spotify_urls.append([])

    df['spotify_urls'] = spotify_urls
    return df


def getTrackInfo(df):
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials("57e2e871e3524493b35ed78cc1661bd7",
                                                                                  "8ee934b00bde4dbe8aa649c9c9c1e77f"))
    df['song_title'], df['artist_name'], df['song_popularity'] , df['danceability'],  df['energy'] , = "", "", "", "" , ""
    df['key'], df['loudness'], df['speechiness'], df['acousticness'], df['instrumentalness'] = "", "", "", "", ""
    df['liveness'], df['valence'] , df['tempo'] = "", "", ""

    for index, row in df.iterrows():
        # try:
            # if len(row['Spotify Link']) > 0:
                # spotifyinfo.append(spotify.track(row['spotify_urls'][0]))
                spotify_track_info = spotify.track(row['Spotify Link'])
                df.loc[index, 'song_title'] = spotify_track_info['name']

                artistlist = []
                for artist in spotify_track_info['artists']:
                    artistlist.append(artist['name'])
                df.at[index, 'artist_name'] = artistlist
                df.loc[index, 'song_popularity'] = spotify_track_info['popularity']
                # AUDIO FEATURES
                audiofeatures = []

                energy = []
                danceability = []
                key = []
                loudness = []
                speechiness = []
                acousticness = []
                instrumentalness = []
                liveness = []
                valence = []
                tempo = []

                ft = spotify.audio_features(row['Spotify Link'])
                features = ft[0]

                energy.append(features['energy'])
                danceability.append(features['danceability'])
                key.append(features['key'])
                loudness.append(features['loudness'])
                speechiness.append(features['speechiness'])
                acousticness.append(features['acousticness'])
                instrumentalness.append(features['instrumentalness'])
                liveness.append(features['liveness'])
                valence.append(features['valence'])
                tempo.append(features['tempo'])

                audiofeatures.append(ft)
                # 'danceability', 'key' , 'loudness' , 'speechiness', 'acousticness' , 'instrumentalness' , 'liveness' , 'valence' , 'tempo'

                df.at[index, 'danceability'] = danceability
                df.at[index, 'energy'] = energy
                df.at[index, 'key'] = key
                df.at[index, 'loudness'] = loudness
                df.at[index, 'speechiness'] = speechiness
                df.at[index, 'acousticness'] = acousticness
                df.at[index, 'instrumentalness'] = instrumentalness
                df.at[index, 'liveness'] = liveness
                df.at[index, 'valence'] = valence
                df.at[index, 'tempo'] = tempo

    return df

def getArtistFollowers(df):
    df['followers'] = ""
    for index, row in df.iterrows():
        song = spotify.track(row['Spotify Link'])
        followers = spotify.artist(song['artists'][0]['uri'])['followers']['total']
        df.at[index,'followers'] = followers
    return df


if __name__ == "__main__":
    # spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials("57e2e871e3524493b35ed78cc1661bd7",
    #                                                                               "8ee934b00bde4dbe8aa649c9c9c1e77f"))

    # df = getTrackInfo(df)
    # df= getArtistFollowers(df)
    # audio_dict = df
    # filename = 'Audio Features All'
    # outfile = open(filename, 'wb')
    # pickle.dump(audio_dict, outfile)
    # outfile.close()

    print("Debugging Message")
