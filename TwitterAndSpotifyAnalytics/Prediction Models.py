import pandas as pd
import math
from statistics import mean
from keras.losses import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import tensorflow as tf
from tensorflow.keras.models import  Sequential
from tensorflow.keras.layers import Dense,Dropout,LSTM
import numpy as np



if __name__ == "__main__":
    songdata = pd.read_pickle("./Audio Features All")
    songdata = songdata.drop([37],axis=0).reset_index(drop=True)
    sentimentdata = pd.read_pickle("./Sentiment Analysis Features")
    tweets = pd.read_pickle('Tweets Metrics top 100')
    songdata['ranking'] = ""


    #Unfolding the Values in the Audio Dataframe
    for i in range(99):
            songdata.at[i, 'danceability'] = songdata.at[i,'danceability'][0]
            songdata.at[i, 'energy'] = songdata.at[i, 'energy'][0]
            songdata.at[i, 'key'] = songdata.at[i, 'key'][0]
            songdata.at[i, 'loudness'] = songdata.at[i, 'loudness'][0]
            songdata.at[i, 'speechiness'] = songdata.at[i, 'speechiness'][0]
            songdata.at[i, 'acousticness'] = songdata.at[i, 'acousticness'][0]
            songdata.at[i, 'instrumentalness'] = songdata.at[i, 'instrumentalness'][0]
            songdata.at[i, 'liveness'] = songdata.at[i, 'liveness'][0]
            songdata.at[i, 'valence'] = songdata.at[i, 'valence'][0]
            songdata.at[i, 'tempo'] = songdata.at[i, 'tempo'][0]

    songdata = pd.concat([songdata, sentimentdata], axis=1)
    songdata = songdata.drop([59], axis=0).reset_index(drop=True)

    # average = mean(popularity)

    for index, row in songdata.iterrows():
        if (row['Rank'] <= 33):
            songdata.at[index, 'ranking']= 1
        elif (row['Rank'] <= 67):
            songdata.at[index, 'ranking']= 2
        else:
            songdata.at[index, 'ranking'] = 3
        # if  (row['tempo'] > 124):
        #  songdata.at[index,'tempo']= (row['tempo'] / 2)

    #     # else:
    #     #     songdata.at[index, 'ranking']= 3



    songdata['fear'] = sentimentdata['fear']
    songdata['anger'] = sentimentdata['anger']
    songdata['trust'] = sentimentdata['trust']
    songdata['surprise'] = sentimentdata['surprise']
    songdata['positive'] = sentimentdata['positive']
    songdata['negative'] = sentimentdata['negative']
    songdata['sadness'] = sentimentdata['sadness']
    songdata['disgust'] = sentimentdata['disgust']
    songdata['joy'] = sentimentdata['joy']
    songdata['anticipation'] = sentimentdata['anticipation']
    songdata['likes'] = tweets['likes']
    songdata['retweets'] = tweets['retweets']
    songdata['quotes'] = tweets ['quotes']

    for index, row in songdata.iterrows():
        songdata.at[index,'likes'] = row['likes'] / row['Number of Tweets']
        songdata.at[index, 'retweets'] = row['retweets'] / row['Number of Tweets']
        songdata.at[index, 'quotes'] = row['quotes'] / row['Number of Tweets']


    X = songdata.drop('Rank', axis=1).drop('ranking', axis = 1).drop('Spotify Link', axis=1).drop('artist_name', axis=1).drop('song_title', axis=1).drop('path', axis=1)#.drop('song_popularity', axis=1)
    y = songdata['ranking']
    y = y.astype('int')

    # X, y = make_classification()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

    #preprocessing
    # sc = StandardScaler()
    # scaler = sc.fit(X_train)
    # trainX_scaled = sc.transform(X_train)
    # testX_scaled = sc.transform(X_test)


    # sel = SelectKBest(score_func=f_classif, k=20)
    # fit = sel.fit(X,y)
    # X= fit.transform(X)

    model = LogisticRegression(solver='lbfgs')
    rfe = RFE(model, n_features_to_select=26)
    fit = rfe.fit(X, y)
    X= fit.transform(X)

    # sc = StandardScaler()
    # scaler = sc.fit(X_train)
    # trainX_scaled = fit.transform(X_train)
    # testX_scaled = fit.transform(X_test)



    #Implementation
    svm = SVC(kernel='linear', C=1)
    svm.fit(X_train, y_train)

    # clf = GaussianNB()
    # clf.fit(X_train, y_train)
    # y_predict = clf.predict(X_test)

    # clf = RandomForestClassifier(n_estimators=100, criterion="entropy", class_weight = "balanced_subsample", max_features="sqrt")
    # clf.fit(X_train, y_train)
    # y_predict = clf.predict(X_test)

    # clf = GradientBoostingClassifier(n_estimators=250, criterion = 'friedman_mse', max_depth = 5, max_features = 'log2')
    # clf.fit(X_train, y_train)
    # y_predict = clf.predict(X_test)

    # clf = ExtraTreesClassifier(n_estimators=100,class_weight="balanced", criterion="entropy", max_depth=50, max_features="sqrt")
    # clf.fit(X_train, y_train)
    # y_predict = clf.predict(X_test)

    # clf = MLPClassifier(hidden_layer_sizes=(150,100,50), max_iter=500,activation='logistic',learning_rate='constant', solver='lbfgs')
    # clf.fit(trainX_scaled, y_train)
    # y_pred = clf.predict(testX_scaled)
    # parameters = {
    #     'learning_rate': ["constant", "invscaling", "adaptive"],
    #     'hidden_layer_sizes': [(100,),(26,78),(150,100,50),(128,64,32,2)],
    #     'max_iter': [300,500,1000,10000],
    #     'activation': ["logistic", "relu", "Tanh"],
    #     'solver' : ['adam', 'lbfgs', 'sgd'],}

    # parameters = {
    #     # 'criterion': ["gini", "entropy"],
    #     'kernel' : ["linear", "poly", "rbf", "sigmoid", "precomputed"],
    #     'gamma' : ["scale", "auto"],
    #     # 'n_estimators': [(100), (50), (150), (250),(400)],
    #     # 'max_features': ["auto", "sqrt", "log2"],
    #     "degree": [(1),(2),(3),(4),(5),(6),(10),(15),(20),(50)],
    #     "class_weight" : ["balanced", "balanced_subsample"],
    #     "break_ties" : ["True","False"]
    # }
    #
    # grid = GridSearchCV(estimator=SVC(), param_grid=parameters)
    # grid.fit(X, y)
    # print(grid.best_score_)
    # print(grid.best_params_)





    scores = cross_val_score(svm, X, y, cv=10)
    print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
    y_pred = cross_val_predict(svm, X, y, cv=10)

    #
    #
    #
    print('Confusion Matrix: ')
    print(confusion_matrix(y,y_pred))
    print('Classification Report ,SVM Model, 3 classes: ')
    print(classification_report(y,y_pred))
    # print('Accuracy of SVM classifier on training set: {:.2f}'
    #       .format(svm.score(X_train, y_train)))
    # print('Accuracy of SVM classifier on test set: {:.2f}'
    #       .format(svm.score(X_test, y_test)))
    # print('Accuracy of Gaussian Naive Bayes Model : {:.2f}'
    #       .format(accuracy_score(y_test, y_predict)))
    print('Accuracy of Model after Cross Validation: {:.2f}'
          .format(accuracy_score(y, y_pred)))



print('Debugging Message')