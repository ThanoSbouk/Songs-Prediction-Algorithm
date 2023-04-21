import glob
import json
import os
import re
import pandas as pd
import pickle
# from SentAnalysis import TweetsSentAnalysis , StringAnalysis



def concat_internal_lists(dict1, dict2, field):
    if field not in dict1 and field in dict2:
        dict1[field] = dict2[field]
    elif field in dict2:
        dict1[field] += dict2[field]

    return dict1


def concat_json_responses(dict1, dict2):
    if 'data' in dict2:
        dict1['data'] += dict2['data']

        dict1['includes'] = concat_internal_lists(dict1['includes'], dict2['includes'], 'media')
        dict1['includes'] = concat_internal_lists(dict1['includes'], dict2['includes'], 'users')
        dict1['includes'] = concat_internal_lists(dict1['includes'], dict2['includes'], 'tweets')
        dict1['includes'] = concat_internal_lists(dict1['includes'], dict2['includes'], 'places')
        dict1['includes'] = concat_internal_lists(dict1['includes'], dict2['includes'], 'polls')

        dict1['meta']['oldest_id'] = dict2['meta']['oldest_id']
        dict1['meta']['result_count'] += dict2['meta']['result_count']  # Adds the new tweets

    return dict1


def concat_json_files(filespath, k):
    os.chdir(filespath)

    extension = 'json'
    all_files = [i for i in glob.glob('*.{}'.format(extension))]
    all_files = all_files[0:k] if k > 0 else all_files

    for file in all_files:
        if all_files.index(file) == 0:
            with open(all_files[0], encoding='utf-8') as fh:
                merged_json = json.load(fh)
        else:
            with open(file, encoding='utf-8') as fh:
                concat_json_responses(merged_json, json.load(fh))

    return merged_json


def retrieveRetweetsFullText(df):
    # TODO
    not_found_tweets = 0
    for index, row in df.iterrows():
        if not pd.isna(row['referenced_tweets']) and row['referenced_tweets'][0]['type'] == 'retweeted':
            referenced_tweet_id = row['referenced_tweets'][0]['id']

            original_tweet = df.loc[df['id'] == referenced_tweet_id]
            if not original_tweet.empty:
                row['text'] = original_tweet['text'].item()
            else:
                not_found_tweets += 1
            print(index, len(df.index))
    print("Not found tweets:", not_found_tweets)

    return df


def retrieveSpotifyUrls(df):
    entities_list = list(df["entities"].to_dict().values())

    spotify_urls = []
    # for i in range(len(entities_list)-1):
    #     spotify_urls.append([-1])

    for idx, d in enumerate(entities_list):
        if not pd.isna(d) and 'urls' in d:  # pd.isna(d) is needed due to truncated retweets
            tweetsUrls = []
            for url in d['urls']:
                if "open.spotify.com/track" in url['expanded_url']:
                    tweetsUrls.append(re.sub(r'\?\S*', '', url['expanded_url']))
            spotify_urls.append(tweetsUrls)
        else:
            spotify_urls.append([-1])

    df['spotify_urls'] = spotify_urls
    return df

def concatTweets(df):
    tweetslist = []
    for index, row in df.iterrows():

        tweetslist.append(row['text'])
    concated_string = '.'.join(tweetslist)

        # tweetslist = df['text']

    return concated_string

def CalculateTweetMetrics(df):
    retweets = list()
    likes = list()
    quotes = list()
    df['retweets'], df['likes'], df['quotes'] = "", "", ""
    for index, row in df.iterrows():
        retweets.append(row['public_metrics']['retweet_count'])
        likes.append(row['public_metrics']['like_count'])
        quotes.append(row['public_metrics']['quote_count'])

    df['retweets'] = retweets
    df['likes'] = likes
    df['quotes']=quotes

    return df


if __name__ == "__main__":
    with open('properties.json') as f:
        properties = json.load(f)
        filePaths = properties["filePath"]

    # scores = list()
    # totaltweets = list()
    # totallikes = list()
    # totalretweets = list()
    # totalquotes = list()
    # tweets_df = pd.DataFrame()
    # tweets_df['likes'], tweets_df['retweets'], tweets_df['quotes'] ,tweets_df['path'] = "","","",""
    # sentiment_df['path'], sentiment_df['Number of Tweets'], sentiment_df['Sentiment Analysis Score'] = "", "", ""

    for path in filePaths:
        data_dict = concat_json_files(path, -1)
        data_df = pd.DataFrame.from_dict(data_dict['data'])
        metadata_tweets_df = pd.DataFrame.from_dict(data_dict['includes']['tweets'])
        # data_df = CalculateTweetMetrics(metadata_tweets_df)
        # totallikes.append(data_df['likes'].sum())
        # totalretweets.append(data_df['retweets'].sum())
        # totalquotes.append(data_df['quotes'].sum())
        metadata_media_df = pd.DataFrame.from_dict(data_dict['includes']['media'])
        metadata_users_df = pd.DataFrame.from_dict(data_dict['includes']['users'])
        metadata_places_df = pd.DataFrame.from_dict(data_dict['includes']['places'])
        metadata_polls_df = pd.DataFrame.from_dict(data_dict['includes']['polls'])
        # tweetsnumber = data_df.shape[0]
        # totaltweets.append(tweetsnumber)
    #     bigtext = concatTweets(data_df)
    #     fullscore= StringAnalysis(bigtext)
    #     scores.append(fullscore)

    # tweets_df['path'] = filePaths
    # tweets_df['likes'] = totallikes
    # tweets_df['retweets'] = totalretweets
    # tweets_df['quotes'] = totalquotes


    # sentiment_df['Number of Tweets'] = totaltweets
    # sentiment_df['Sentiment Analysis Score'] = scores

    # dict = tweets_df
    # filename = 'Tweets Metrics 61'
    # outfile = open(filename,'wb')
    # pickle.dump(dict,outfile)
    # outfile.close()

    # data_df = TweetsSentAnalysis(data_df)


    print("Debugging Message")
