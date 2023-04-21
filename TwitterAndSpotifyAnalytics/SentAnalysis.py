import json
from nrclex import NRCLex
import pandas as pd
import pickle




# audio_df=pd.read_pickle("./Audio Features")
one_df = pd.read_pickle('Tweets Metrics top 100')
two_df = pd.read_pickle('Audio Features All')
three_df = pd.read_pickle('Sentiment Analysis Features')
sentiment_df= pd.concat([one_df,two_df,three_df],axis=0,ignore_index=True)
# audio_df['Sentiment Score']= ''
# for index, row in audio_df.iterrows():
#         audio_df.at[index,'Sentiment Score'] = 1
# with open('properties.json') as f:
#     properties = json.load(f)
#     filePath = properties["filePath"]
# sent_df = pd.read_pickle(filePath + "/Sentiment Analysis_Blinding Lights")

def TweetsSentAnalysis(df):
    df['SentScore'] = ''
    for index, row in df.iterrows():
        tweet=row['text']
        emotion = NRCLex(tweet)
        df.at[index, 'SentScore'] = emotion.affect_frequencies


    return df

def StringAnalysis(str):
    emotion= NRCLex(str)
    score = emotion.affect_frequencies
    # audio_df = pd.read_pickle("./Audio Features")
    # audio_df['Sentiment Score']= ''
    # for index, row in audio_df.iterrows():
    #     audio_df.at[index,'Sentiment Score'] = score

    return score

def ExtractSentiments(df):
    df['fear'], df['anger'], df['trust'],df['surprise'],df['positive'],df['negative'],df['sadness'] ="","","","","","",""
    df['disgust'], df['joy'], df['anticipation'] = "","","",

    for index, row in df.iterrows():
        nrc= row['Sentiment Analysis Score']
        df.at[index,'fear']= nrc['fear']
        df.at[index, 'anger'] = nrc['anger']
        df.at[index, 'trust'] = nrc['trust']
        df.at[index, 'surprise'] = nrc['surprise']
        df.at[index, 'positive'] = nrc['positive']
        df.at[index, 'negative'] = nrc['negative']
        df.at[index, 'sadness'] = nrc['sadness']
        df.at[index, 'disgust'] = nrc['disgust']
        df.at[index, 'joy'] = nrc['joy']
        df.at[index, 'anticipation'] = nrc['anticipation']
    return df


# sentiment_df= ExtractSentiments(sentiment_df)
# del sentiment_df['Sentiment Analysis Score']
# sent_dict = sentiment_df
# filename = 'Tweets Metrics top 100'
# outfile = open(filename,'wb')
# pickle.dump(sent_dict,outfile)
# outfile.close()


print('Debugging Message')


