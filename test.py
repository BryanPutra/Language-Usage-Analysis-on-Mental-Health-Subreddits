from sklearn import metrics
from sklearn.pipeline import Pipeline

import nltk
from pandas.core.frame import DataFrame

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import RocCurveDisplay,classification_report,ConfusionMatrixDisplay, confusion_matrix, accuracy_score
from sklearn.linear_model import SGDClassifier
import sklearn.metrics as met
import matplotlib.pyplot as plt
from Pipeline.plotUtility import showConfusionMatrix
from nltk.corpus import stopwords 
import DataUtil.dataframeUtility as dfUtil

subreddits = ['suicideWatch', 'depression']
features = ['Title', 'Content']

df, selectedColumn = dfUtil.createDataframe(subreddits, features)
X = df[selectedColumn]
y = df['Label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    
clf = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SGDClassifier())
])

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print(classification_report(y_test, y_pred))
