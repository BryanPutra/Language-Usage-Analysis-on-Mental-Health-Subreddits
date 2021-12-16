import pandas as pd
import os.path
import emoji
import re
import contractions
from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
import string

lemmatizer = WordNetLemmatizer()
nltkStopWords = stopwords.words('english')
spelling = SpellChecker('en')

# we don't want to remove negation words because those words are important to understand the context of the content
# so we remove the negation words that are in the stopwords list
nltkStopWords.remove("not")
nltkStopWords.remove("nor")
nltkStopWords.remove("no")
def fillColumnWithEmptyString(df, column):
    df[column].fillna(value = "", inplace=True)
    return df

def fillColumnWithAverage(df, column):
    df[column].fillna(value = df[column].mean(), inplace=True)
    return df

def fillColumnWithMode(df, column):
    df[column].fillna(value = df[column].mode().sample(n=1, random_state=1), inplace=True)
    return df

def dropRowOnEmptyColumn(df, column):
    df[column].dropna(subset = column, inplace=True)
    return df

def removePunctuationInColumn(df, column):
    df[column] = df[column].str.replace(r'[^\w\s]','')
    return df

def addPrefixToStringColumn(df, column, prefix):
    df[column] = prefix + df[column].astype(str)
    return df[column]

def expandContractions(text):
    result = []
    textList = text.split()
    for word in textList:
        result.append(contractions.fix(word))
    resultString = ' '.join(result)
    return resultString

def createDataframe(subredditList : list, featureColumnList : list, nrows : int = 5000):
    df = []
    label = {}
    featureColumn = 'Feature' + ''.join(featureColumnList)
    
    # Combines all the file into one big dataframe
    for count, s in enumerate(subredditList):
        df.append(pd.read_csv(os.path.dirname(__file__) + '/../Datasets/' + s + 'BigCleaned.csv', nrows=nrows))
        label[s] = count
    df = pd.concat(df)
    df[featureColumn] = ""

    for count, j in enumerate(featureColumnList):
        df = fillColumnWithEmptyString(df, j)
        if(count != 0):
            df[featureColumn] += addPrefixToStringColumn(df, j, prefix = ' ')
        else:
            df[featureColumn] += df[j]
    
    # Creates a new column based on the combined features
    removePunctuationInColumn(df, featureColumn)
    df.dropna(subset=[featureColumn], inplace=True)
    # Preprocessing goes here
    df[featureColumn] = df[featureColumn].map(lambda x: removeEmoji(x))
    df[featureColumn] = df[featureColumn].map(lambda x: expandContractions(x))
    df[featureColumn] = df[featureColumn].map(lambda x: processContent(x))
    
    df['Label'] = df['Subreddit'].map(label)
    df = df.sample(frac = 1)
    df.info()
    return df, featureColumn

def removeEmoji(text):
    text = emoji.demojize(text)
    text = re.sub(r'(:[!_\-\w]+:)', '', text)
    return text

def lemmatizeWords(textList):
    lemmatized = []
    textWithTag = pos_tag(textList)
    for word, tag in textWithTag:
        tag = tag[0].lower()
        tag = tag if tag in ['a', 'r', 'n', 'v'] else None 
        lemmatized.append(lemmatizer.lemmatize(word, tag) if tag else word)
    lemmatizedString = ' '.join(lemmatized)
    return lemmatizedString

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

def removeStopWords(textList):
    removed = []
    for word in textList:
        if word not in nltkStopWords:
            removed.append(word)
    return removed

def processContent(text):
    tokenized = word_tokenize(text)
    # result = removeStopWords(tokenized)
    result = lemmatizeWords(tokenized)
    return result