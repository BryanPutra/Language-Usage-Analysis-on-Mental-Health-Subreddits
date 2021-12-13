
import pandas as pd
import nltk
import contractions
import dataframeUtility
import emoji
import re
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
from sklearn.feature_extraction.text import CountVectorizer
from spellchecker import SpellChecker
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
nltkStopWords = stopwords.words('english')
spelling = SpellChecker('en')
# we don't want to remove negation words because those words are important to understand the context of the content
# so we remove the negation words that are in the stopwords list
nltkStopWords.remove("not")
nltkStopWords.remove("nor")
nltkStopWords.remove("no")

def removeEmoji(text):
    text = emoji.demojize(text)
    text = re.sub(r'(:[!_\-\w]+:)', '', text)
    return text

def checkSpelling(text):
    correctResult = []
    wordList = text.split()
    typoWords = spelling.unknown(wordList)
    for word in wordList:
        if word in typoWords:
            correctResult.append(spelling.correction(word))
        else:
            correctResult.append(word)
    resultString = ' '.join(correctResult)
    return resultString

def removePunctuation(text):
    newText = text.translate(str.maketrans('', '', string.punctuation))
    return newText

def expandContractions(text):
    result = []
    textList = text.split()
    for word in textList:
        result.append(contractions.fix(word))
    resultString = ' '.join(result)
    return resultString

def removeStopWords(textList):
    removed = []
    for word in textList:
        if word not in nltkStopWords:
            removed.append(word)
    return removed

def lemmatizeWords(textList):
    lemmatized = [lemmatizer.lemmatize(word) for word in textList]
    lemmatizedString = ' '.join(lemmatized)
    return lemmatizedString

def processContent(text):
    tokenized = word_tokenize(text)
    result = removeStopWords(tokenized)
    result = lemmatizeWords(result)
    return result

set to when calling a dataframe, it displays all the columns
pd.set_option('display.max_columns', None)
dfSuicideWatch = pd.read_csv('./Datasets/suicideWatchCleaned.csv', low_memory=False)
dfDepression = pd.read_csv('./Datasets/depressionCleaned.csv', low_memory=False)
df = pd.concat([dfSuicideWatch, dfDepression])

df['Label'] = df['Subreddit'].map({'depression' : 0, 'suicideWatch' : 1})

dataframeUtility.fillColumnWithEmptyString(df, 'Content')
dataframeUtility.addPrefixToStringColumn(df, 'Content', ' ')
df['TitleAndContent'] = df['Title'] + df['Content'] 
# dataframeUtility.removePunctuationInColumn(df, 'TitleAndContent')

df['TitleAndContent'] = df['TitleAndContent'].map(lambda x: removeEmoji(x))
df['TitleAndContent'] = df['TitleAndContent'].map(lambda x: expandContractions(x))
# check spelling takes 1 year to finish omegalul
# df['TitleAndContent'] = df['TitleAndContent'].map(lambda x: checkSpelling(x))
df['TitleAndContent'] = df['TitleAndContent'].map(lambda x: processContent(x))
print(df.head(10)['TitleAndContent'])


