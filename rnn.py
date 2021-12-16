from re import S
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import DataUtil.dataframeUtility as dfUtil
from tqdm import tqdm
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras.layers import Dense, Dropout, LSTM, Embedding, Bidirectional, SimpleRNN

EMBEDDING_SIZE = 300
VOCABULARY_SIZE = 10000
SEQUENCE_LENGTH = 300
def load_data(subredditList, featureColumnList):
    df, selectedColumn = dfUtil.createDataframe(subredditList, featureColumnList, 25000)

    tokenizer = Tokenizer(num_words=VOCABULARY_SIZE, oov_token="<OOV>")
    tokenizer.fit_on_texts(df[selectedColumn])

    X = tokenizer.texts_to_sequences(df[selectedColumn])
    X = pad_sequences(X, maxlen=SEQUENCE_LENGTH, padding='pre', truncating='post')
    y = to_categorical(df['Label'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    data = {}
    data["X_train"] = X_train
    data["X_test"]= X_test
    data["y_train"] = y_train
    data["y_test"] = y_test
    data["tokenizer"] = tokenizer
    data["int2label"] =  {0: "Depression", 1: "SuicideWatch"}
    data["label2int"] = {"Depression": 0, "SuicideWatch": 1}
    
    return data

def get_embedding_vectors(word_index, embedding_size=EMBEDDING_SIZE):
    embedding_matrix = np.zeros((len(word_index) + 1, embedding_size))
    with open(f"GloVe/glove.6B.{embedding_size}d.txt", encoding="utf8") as f:
        for line in tqdm(f, "Reading GloVe"):
            values = line.split()
            # get the word as    the first word in the line
            word = values[0]
            if word in word_index:
                idx = word_index[word]
                # get the vectors as the remaining values in the line
                embedding_matrix[idx] = np.array(values[1:], dtype="float32")
    return embedding_matrix

def create_model(word_index,
                unit=128,
                embedding_size=EMBEDDING_SIZE, sequence_length=SEQUENCE_LENGTH, dropout=0.4, 
                loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.001), 
                output_length=2):
    embedding_matrix = get_embedding_vectors(word_index, embedding_size)
    model = Sequential()
    # add the embedding layer
    model.add(Embedding(len(word_index) + 1,
              embedding_size,
              weights=[embedding_matrix],
              trainable=False,
              input_length=sequence_length))
    # model.add(Embedding(len(word_index) + 1, embedding_size, input_length=sequence_length))
    model.add(LSTM(unit, return_sequences=True))
    model.add(LSTM(unit, return_sequences=True))
    model.add(LSTM(unit, return_sequences=False))
    model.add(Dense(output_length, activation="sigmoid"))
    # model.add(Dense(output_length, activation="relu"))
    # Compile the model
    model.compile(optimizer=optimizer, loss=loss, metrics=["accuracy"])
    return model

subreddits = ['SuicideWatch', 'Depression']
features = ['Title', 'Content']

data = load_data(subreddits, features)
model = create_model(data["tokenizer"].word_index)
model.summary()

history = model.fit(data["X_train"], data["y_train"],
                    batch_size=128,
                    epochs=15,
                    validation_data=(data["X_test"], data["y_test"]),
                    verbose=1)

model.save(os.path.join("ModelResult", "yeah") + ".h5")