import pandas as pd
import os.path

from pandas.core.frame import DataFrame
import DataUtil.dataframeUtility as dataframeUtility
from Pipeline.cvec import cvec

from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier

suicide_df = pd.read_csv(os.path.dirname(__file__) + '/SuicideWatchCleaned.csv')
depression_df = pd.read_csv(os.path.dirname(__file__) + '/DepressionCleaned.csv')

df = pd.concat([suicide_df, depression_df])
df = df.sample(frac=1)

df['Label'] = df['Subreddit'].map({'depression' : 0, 'suicideWatch' : 1})

selectedColumn = 'TitleAndContent'

dataframeUtility.fillColumnWithEmptyString(df, 'Content')
dataframeUtility.addPrefixToStringColumn(df, 'Content', ' ')
df[selectedColumn] = df['Title'] + df['Content'] 
dataframeUtility.removePunctuationInColumn(df, selectedColumn)

cvec(df, selectedColumn, 'Label', MultinomialNB())