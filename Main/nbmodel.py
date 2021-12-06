import pandas as pd
import os.path
import dataframeUtility

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

cv = CountVectorizer()
suicide_df = pd.read_csv(os.path.dirname(__file__) + '/../SuicideWatchCleaned.csv')
depression_df = pd.read_csv(os.path.dirname(__file__) + '/../DepressionCleaned.csv')

df = pd.concat([suicide_df, depression_df])

df['Label'] = df['Subreddit'].map({'depression' : 0, 'suicideWatch' : 1})

dataframeUtility.fillColumnWithEmptyString(df, 'Content')
dataframeUtility.addPrefixToStringColumn(df, 'Content', ' ')
df['TitleAndContent'] = df['Title'] + df['Content'] 
dataframeUtility.removePunctuationInColumn(df, 'TitleAndContent')

print(df.head(10)['TitleAndContent'])

X = df['TitleAndContent']
y = df['Label']

X = cv.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

clf = MultinomialNB()
clf.fit(X_train, y_train)
clf.score(X_test, y_test)

y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred)) 