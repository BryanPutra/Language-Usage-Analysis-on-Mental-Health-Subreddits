from matplotlib.pyplot import axis
import pandas as pd
import os.path

from pandas.core.frame import DataFrame
import DataUtil.dataframeUtility as dfUtil
from Pipeline.vectorizers import cvec, tfidf

from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier

subreddits = ['suicideWatch', 'depression', 'CasualConversation']
features = ['Content']

df, selectedColumn = dfUtil.createDataframe(subreddits, features)

tfidf(df, selectedColumn, 'Label', NuSVC())