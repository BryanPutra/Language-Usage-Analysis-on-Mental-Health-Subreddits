import pandas as pd
import os.path

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
    df[column] = df[column].str.replace('[^\w\s]','')
    return df

def addPrefixToStringColumn(df, column, prefix):
    df[column] = prefix + df[column].astype(str)
    return df[column]


def createDataframe(subredditList : list, featureColumnList : list):
    df = []
    label = {}
    featureColumn = 'Feature' + ''.join(featureColumnList)
    
    # Combines all the file into one big dataframe
    for count, s in enumerate(subredditList):
        df.append(pd.read_csv(os.path.dirname(__file__) + '/../Datasets/' + s + 'Cleaned.csv'))
        label[s] = count
    df = pd.concat(df)
    
    # Creates a new column based on the combined features
    df[featureColumn] = ""
    for count, i in enumerate(featureColumnList):
        df = fillColumnWithEmptyString(df, i)
        if(count != 0):
            df[featureColumn] += addPrefixToStringColumn(df, i, prefix = ' ')
        else:
            df[featureColumn] += df[i]
    removePunctuationInColumn(df, featureColumn)
    
    # Preprocessing goes here
    df['Label'] = df['Subreddit'].map(label)
    df = df.sample(frac = 1)
    return df, featureColumn
    