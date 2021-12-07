from pandas.core.frame import DataFrame

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import RocCurveDisplay,classification_report,ConfusionMatrixDisplay
import matplotlib.pyplot as plt

from nltk.corpus import stopwords 
nltkStopWords = stopwords.words('english')
nltkStopWords.remove("not")
nltkStopWords.remove("nor")
nltkStopWords.remove("no")

def cvec(df : DataFrame, xColumn : str, yColumn : str, clf):
    cv = CountVectorizer()
    X = df[xColumn]
    y = df[yColumn]
    X = cv.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    clf.fit(X_train, y_train)
    clf.score(X_test, y_test)

    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred)) 
   
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,5))

    ConfusionMatrixDisplay.from_predictions(y_test, y_pred, ax= ax1)
    RocCurveDisplay.from_predictions(y_test, y_pred, ax = ax2)
    
    plt.show()
    