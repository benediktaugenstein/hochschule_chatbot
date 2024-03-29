# Importieren von genutzten Softwarebibliotheken
import os
import sys
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelBinarizer
import pandas as pd
from myfuncs import *
from flask import Flask, render_template, request, session

# Festlegung relevanter Variablen
app = Flask(__name__)
model = keras.models.load_model('models/hs_chatbot.h5')
model2 = keras.models.load_model('models/bib.h5')
link_general = 'data/general.csv'
link_bib = 'data/bib.csv'
models = [model, model2]
datasets = [link_general, link_bib]
tokenizers = []
word_indices = []
sequences_array = []
lengths_input = []
labels_transformed_array = []

app.secret_key='test'

#Tokenisierung der möglichen Eingaben sowie Encodierung (one-hot encoding) der möglichen Ausgabewerte (Labels) für die unterschiedlichen Modelle
for i, model in enumerate(models):
  data = pd.read_csv(datasets[i])

  sentences = data['Input']
  labels = data['Output']

  #tokenizer = Tokenizer(num_words = 100)
  tokenizer = Tokenizer()
  tokenizer.fit_on_texts(sentences)
  word_index = tokenizer.word_index
  sequences = tokenizer.texts_to_sequences(sentences)

  tokenizers.append(tokenizer)
  word_indices.append(word_index)

  sequences = pad_sequences(sequences, padding='post', truncating='post')
  sequences_array.append(sequences)

  #word_count = len(word_index)
  len_input = len(sequences[0])
  lengths_input.append(len_input)
  if i == 0: # General
    ohe = LabelBinarizer()
    labels_transformed_general = ohe.fit_transform(labels)
  else: # Feeling
    ohe2 = LabelBinarizer()
    labels_transformed_feeling = ohe2.fit_transform(labels)

# Festlegung des templates zum Anzeigen der Web-App
@app.route('/')
def my_form():
    return render_template('input.html')

# Ermittlung der Nutzereingabe sowie Ermittlung der Antwort
@app.route('/', methods=['POST'])
def output():
    text = request.form['text'] # Ermittlung der Eingabe aus dem Template
    if text == '':
      result = 'Bitte gib eine Nachricht ein.'
      initial_text = text
    else:
      initial_text = text
      result = new_input(text, tokenizers, lengths_input, models, ohe, ohe2) # Diese Funktion befindet sich in myfuncs.py, hier werden Vorhersagen durch die Modelle getroffen
      
    # Kombination der Eingaben und der Antwort mit vorherigen Eingaben und Antworten (um den "Chatverlauf" sehen zu können)
    if 'fin_output' in session:
      session['fin_output'] = session['fin_output'] + '<br></br>Du: ' + initial_text + '<br>' + 'Chatbot: ' + result
    else:
      session['fin_output'] = '<br></br>Du: ' + initial_text + '<br>' + 'Chatbot: ' + result
    
    var = session['fin_output']
    result = str(var)
    
    # Ausgabe im HTML-Template
    return render_template("input.html",result = result)

#if __name__ == '__main__':
    #app.run()
