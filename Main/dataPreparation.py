
import pandas as pd
import string
import nltk
import contractions
# nltk.download('punkt')
# nltk.download('stopwords')
from sklearn.feature_extraction.text import CountVectorizer
from spellchecker import SpellChecker
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer('english')
nltkStopWords = stopwords.words('english')
print(nltkStopWords)
spelling = SpellChecker('en')
# we don't want to remove negation words because those words are important to understand the context of the content
# so we remove the negation words that are in the stopwords list
nltkStopWords.remove("not")
nltkStopWords.remove("nor")
nltkStopWords.remove("no")

def checkSpelling(text):
    correctResult = []
    wordList = text.split()
    typoWords = spelling.unknown(wordList)
    for word in wordList:
        if word in typoWords:
            correctResult.append(spelling.correction(word))
        else:
            correctResult.append(word)
    return " ".join(correctResult)

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

# stopWordsPunctuationRemoved = [removePunctuation(word) for word in nltkStopWords]

dfSuicideWatch = pd.read_csv('./Datasets/SuicideWatchRapi.csv', low_memory=False)
dfIndex = dfSuicideWatch.index

# set to when calling a dataframe, it displays all the columns
pd.set_option('display.max_columns', None)
# print(dfSuicideWatch.head(10))

# get indexes of the rows that have null values and store it to an array
# isNullRow = dfSuicideWatch.isnull().any(axis=1)
# dfNullIndexes = dfIndex[isNullRow]
# dfNullIndexList = dfNullIndexes.tolist()
# print(dfNullIndexList)

# dropping null rows according to the indexes stored from the previous code
dfSuicideWatch.drop(dfNullIndexList, inplace=True)
print(dfSuicideWatch)
# print(dfSuicideWatch.dtypes)

textTest = dfSuicideWatch.at[7, 'Content'].lower()
textTest = expandContractions(textTest).lower()
textTest = checkSpelling(textTest)
print(textTest)

tokenizedTextTest = word_tokenize(textTest)
print(tokenizedTextTest)
filteredWords = []
for word in tokenizedTextTest:
    if word not in stopWordsPunctuationRemoved:
        filteredWords.append(word)
print(filteredWords)
print("\n")
print(len(tokenizedTextTest))
print(len(filteredWords))
stemmedWords = [stemmer.stem(word) for word in filteredWords]
print(stemmedWords)

# using the apply function from pandas dataframe would operate on the whole row
# use .map() instead to operate on once cell at a time
# dfSuicideWatch['Content'].map(lambda content: )
