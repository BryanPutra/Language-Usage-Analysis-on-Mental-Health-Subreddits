import pandas as pd
import os.path

def fillColumnWithEmptyString(df, column):
    df[column].fillna(value = "", inplace=True)
    return df

def fillColumnWithAverage(df, column):
    df[column].fillna(value = df[column].mean(), inplace=True)
    return df

def dropRowOnEmptyColumn(df, column):
    df[column].dropna(subset = column, inplace=True)
    return df

def removePunctuationInColumn(df, column):
    df[column] = df[column].str.replace('[^\w\s]','')
    return df

def addPrefixToStringColumn(df, column, prefix):
    df[column] = prefix + df[column].astype(str)