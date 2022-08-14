# Importieren von genutzten Softwarebibliotheken
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from datetime import datetime, timezone, timedelta

from sklearn.preprocessing import LabelBinarizer

import pandas as pd

# Datensatz einlesen
data = pd.read_csv('/path/to/data/dataset_name.csv')
sentences = data['Sentence'] #Input
labels = data['Result'] #Output

# Wörter in Zahlenwerte umwandeln
tokenizer = Tokenizer()
tokenizer.fit_on_texts(sentences)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(sentences)

# Padding der Eingabesequenzenund
sequences = pad_sequences(sequences, padding='post', truncating='post')

#Wortanzahl ermitteln
word_count = len(word_index)

# Länge der Eingabe ermitteln (Anzahl der Eingabewerte)
len_input = len(sequences[0])

# Lables in Zahlenwerte umwandeln (One-hot)
ohe = LabelBinarizer()
labels_transformed = ohe.fit_transform(labels)
len_output = len(labels_transformed[0])

# Modell erstellen
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=word_count+1, output_dim=16, input_length=len_input),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(24, activation='relu'),
    tf.keras.layers.Dense(24, activation='relu'),
    tf.keras.layers.Dense(len_output, activation='sigmoid')
])

model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
model.summary()

# Anzahl der Epochen und validation split festlegen, Modell trainieren
num_epochs = 50
validation_percentage = 0.2
history = model.fit(sequences, labels_transformed, epochs=num_epochs, verbose=1, batch_size = 20, shuffle=True, validation_split=validation_percentage)

# Modell abspeichern
model.save('/paht/to/folder/model_name.h5')
