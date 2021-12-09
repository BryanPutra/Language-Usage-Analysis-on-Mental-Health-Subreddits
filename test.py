from sklearn import metrics
from sklearn.pipeline import Pipeline

import nltk
from pandas.core.frame import DataFrame

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import RocCurveDisplay,classification_report,ConfusionMatrixDisplay, confusion_matrix, accuracy_score
import sklearn.metrics as met
import matplotlib.pyplot as plt
from Pipeline.plotUtility import showConfusionMatrix
from nltk.corpus import stopwords 
import DataUtil.dataframeUtility as dfUtil

subreddits = ['suicideWatch', 'depression']
features = ['Title', 'Content']

df, selectedColumn = dfUtil.createDataframe(subreddits, features)

clf = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', MultinomialNB())
])

clf.fit(df[selectedColumn], df['Label'])
y_pred = clf.predict(df[selectedColumn])

print(classification_report(df['Label'], y_pred))
