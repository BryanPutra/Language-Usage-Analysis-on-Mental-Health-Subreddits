import pandas as pd
import os.path

from pandas.core.frame import DataFrame
import DataUtil.dataframeUtility as dataframeUtility
from Model.cvec import cvec

from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.metrics import classification_report

suicide_df = pd.read_csv(os.path.dirname(__file__) + '/SuicideWatchCleaned.csv')
depression_df = pd.read_csv(os.path.dirname(__file__) + '/DepressionCleaned.csv')

df = pd.concat([suicide_df, depression_df])
df = df.sample(frac=1)

df['Label'] = df['Subreddit'].map({'depression' : 0, 'suicideWatch' : 1})

dataframeUtility.fillColumnWithEmptyString(df, 'Content')
dataframeUtility.addPrefixToStringColumn(df, 'Content', ' ')
df['TitleAndContent'] = df['Title'] + df['Content'] 
dataframeUtility.removePunctuationInColumn(df, 'TitleAndContent')

cvec(df, 'TitleAndContent', 'Label', NuSVC())