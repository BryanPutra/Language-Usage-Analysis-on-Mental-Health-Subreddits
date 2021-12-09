import matplotlib.pyplot as plt
import os
import re
import shutil
import string
import pandas as pd
import DataUtil.dataframeUtility as dfUtil
import tensorflow_hub as hub
import tensorflow_text
from sklearn.model_selection import train_test_split

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

suicide_df = pd.read_csv(os.path.dirname(__file__) + '/Datasets/suicideWatchCleaned.csv')
depression_df = pd.read_csv(os.path.dirname(__file__) + '/Datasets/depressionCleaned.csv')

suicide_df = suicide_df.sample(depression_df.shape[0])
df = pd.concat([suicide_df, depression_df])
df['Label'] = df['Subreddit'].map({'depression' : 0, 'suicideWatch' : 1})
dfUtil.fillColumnWithEmptyString(df, 'Content')
df['Feature'] = df['Title'] + df['Content']

X_train, X_test, y_train, y_test = train_test_split(df['Feature'], df['Label'], test_size=0.33, random_state=42)

bert_preprocess = hub.KerasLayer('https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3')
bert_encoder = hub.KerasLayer('https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4')

def get_sentence_embedding(sentences):
    preprocessed_text = bert_preprocess(sentences)
    return bert_encoder(preprocessed_text)['pooled_output']

print(get_sentence_embedding(['what fuck', 'yo up for volleyball?']))
