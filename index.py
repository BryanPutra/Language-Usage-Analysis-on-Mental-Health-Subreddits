from matplotlib.pyplot import axis
import pandas as pd
import os.path

from pandas.core.frame import DataFrame
import DataUtil.dataframeUtility as dfUtil
from skLearnPipeline.vectorizers import cvec, tfidf

from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier

subreddits = ['SuicideWatch', 'CasualConversation']
features = ['Title', 'Content']

df, selectedColumn = dfUtil.createDataframe(subreddits, features, 25000)
# df.info()
# df = pd.read_csv(os.path.dirname(__file__) + '/Datasets/' + 'CombinedSubredditBig' + 'Cleaned.csv')
print(df.dropna(subset=['FeatureTitleContent'], inplace=True))
print(df.dropna(subset=['Title'], inplace=True))
print(df.isna().sum())
cvec(df, 'FeatureTitleContent', 'Label', SVC()) 
