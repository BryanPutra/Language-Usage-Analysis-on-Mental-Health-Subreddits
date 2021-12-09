import nltk
from pandas.core.frame import DataFrame

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import RocCurveDisplay,classification_report,ConfusionMatrixDisplay, confusion_matrix, accuracy_score
import sklearn.metrics as met
import matplotlib.pyplot as plt
from Pipeline.plotUtility import showConfusionMatrix

from nltk.corpus import stopwords 
nltkStopWords = stopwords.words('english')
nltkStopWords.remove("not")
nltkStopWords.remove("nor")
nltkStopWords.remove("no")

def generalVectorizer(df, vc, xColumn, yColumn, clf, name):
    X = df[xColumn]
    y = df[yColumn]
    X = vc.fit_transform(X)
    X = TfidfTransformer().fit_transform(X)

    y_pred, y_test = classify(X, y, clf)
    name = name + " "  + clf.__class__.__name__
    showMetrics(name, y_test, y_pred)

def showMetrics(name, y_test, y_pred):
    print(name)

    print("Accuracy : " , met.accuracy_score(y_test, y_pred))
    print("F1 score : " , met.f1_score(y_test, y_pred))
    print("Recall   : " , met.recall_score(y_test, y_pred))
    cm = confusion_matrix(y_test, y_pred)
    for label1, i in enumerate(cm):
        for label2, j in enumerate(i):
            print(label1, label2, ":" ,j)
    showConfusionMatrix(y_test, y_pred)

def cvec(df : DataFrame, xColumn : str, yColumn : str, clf):
    cv = CountVectorizer(strip_accents = 'ascii', stop_words = nltkStopWords)
    generalVectorizer(df, cv, xColumn, yColumn, clf, "count vectorizer")

def tfidf(df : DataFrame, xColumn : str, yColumn : str, clf):
    tfidf = TfidfVectorizer(strip_accents = 'ascii', stop_words = nltkStopWords)
    generalVectorizer(df, tfidf, xColumn, yColumn, clf, "tfidf")

def classify(X, y, clf):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    clf.fit(X_train, y_train)
    clf.score(X_test, y_test)
    y_pred = clf.predict(X_test)
    return y_pred, y_test
