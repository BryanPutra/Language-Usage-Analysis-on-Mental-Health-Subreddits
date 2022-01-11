
import pandas as pd
import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
import contractions
import dataframeUtility as dfUtil
import emoji
import re
import matplotlib.pyplot as plt
import string

from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from spellchecker import SpellChecker
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
nltkStopWords = stopwords.words('english')
spelling = SpellChecker('en')
# set to when calling a dataframe, it displays all the columns
pd.set_option('display.max_columns', None)
# we don't want to remove negation words because those words are important to understand the context of the content
# so we remove the negation words that are in the stopwords list
# not removing for text visualization
# nltkStopWords.remove("not")
# nltkStopWords.remove("nor")
# nltkStopWords.remove("no")

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
        if word.lower() not in nltkStopWords:
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

def processContentDataSet(dataframe):
    dfUtil.fillColumnWithEmptyString(dataframe, 'Content')
    dfUtil.addPrefixToStringColumn(dataframe, 'Content', ' ')
    dataframe['TitleAndContent'] = dataframe['Title'] + dataframe['Content'] 
    dataframe['TitleAndContent'] = dataframe['TitleAndContent'].map(lambda x: removePunctuation(x))
    dataframe['TitleAndContent'] = dataframe['TitleAndContent'].map(lambda x: removeEmoji(x))
    dataframe['TitleAndContent'] = dataframe['TitleAndContent'].map(lambda x: expandContractions(x))
    # check spelling takes 1 year to finish omegalul
    # dataframe['TitleAndContent'] = dataframe['TitleAndContent'].map(lambda x: checkSpelling(x))
    dataframe['TitleAndContent'] = dataframe['TitleAndContent'].map(lambda x: processContent(x))
    return dataframe

def visualizeCloud(dataframe, subredditName, columnName):
    wordcloud = WordCloud(background_color="white",width=1600, height=800).generate(' '.join(dataframe[columnName].tolist()))
    plt.figure( figsize=(20,10), facecolor='k')
    plt.imshow(wordcloud)
    wordcloud.to_file('{}WordsCloud.png'.format(subredditName))
    plt.show()

def getTopWords(corpus, n):
    vec = CountVectorizer().fit(corpus)
    matrixWords = vec.transform(corpus)
    sumOfWords = matrixWords.sum(axis=0) 
    wordsFreq = [(word, sumOfWords[0, index]) for word, index in vec.vocabulary_.items()]
    wordsFreq = sorted(wordsFreq, key = lambda x: x[1], reverse=True)
    return wordsFreq[:n]

def visualizeTopBar(dataframe, subredditName, n):
    topWords = getTopWords(dataframe['TitleAndContent'], n)
    # for word, freq in common_words:
    #     print(word, freq) 
    tempDf = pd.DataFrame(topWords, columns = ['TitleAndContent' , 'Count'])
    tempDf.groupby('TitleAndContent').sum()['Count'].sort_values(ascending=False).plot(kind='bar', ylabel='Count', title='Top 20 words in {}'.format(subredditName))
    plt.savefig('{}TopWordsBar.png'.format(subredditName))
    plt.show()

# def visualizeTotalDataset(dataframe1, dataframe2):
#     dataframe1 
#     df1Count = len(dataframe1.index)
#     df2Count = len(dataframe2.index)
#     tempDf = pd.DataFrame

# dfSuicideWatch = pd.read_csv('./Datasets/suicideWatchCleaned.csv', low_memory=False)
# dfDepression = pd.read_csv('./Datasets/depressionCleaned.csv', low_memory=False)

dfSuicideWatchMale = pd.read_csv('./Datasets/MaleSuicideWatch.csv', low_memory=False)
dfSuicideWatchFemale = pd.read_csv('./Datasets/FemaleSuicideWatch.csv', low_memory=False)
dfDepressionMale = pd.read_csv('./Datasets/MaleDepression.csv', low_memory=False)
dfDepressionFemale = pd.read_csv('./Datasets/FemaleDepression.csv', low_memory=False)
totalMaleRows = len(dfSuicideWatchMale) + len(dfDepressionMale)
totalFemaleRows = len(dfSuicideWatchFemale) + len(dfDepressionFemale)

# dfSuicideWatch = processContentDataSet(dfSuicideWatch)
# dfDepression = processContentDataSet(dfDepression)

# visualizeCloud(dfSuicideWatch, 'SuicideWatch', 'TitleAndContent')
# visualizeCloud(dfDepression, 'Depression', 'TitleAndContent')
# visualizeTopBar(dfSuicideWatch, 'SuicideWatch', 20)
# visualizeTopBar(dfDepression, 'Depression', 20)

# visualize gender difference

columns = ['Male', 'Female']
rows = [totalMaleRows, totalFemaleRows]
plt.bar(columns, rows, color=['lightblue', 'pink'])
plt.title('Gender Comparison in SuicideWatch and Depression Subreddits')
plt.xlabel('Gender')
plt.ylabel('Authors')
plt.savefig('genderComparisonBar.png')
plt.show()