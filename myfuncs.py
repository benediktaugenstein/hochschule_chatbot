def new_input(input_initial, tokenizers, lengths_input, models, ohe, ohe2):
  from tensorflow.keras.preprocessing.sequence import pad_sequences
  from flask import session
  input_prep = [input_initial]
  inp = tokenizers[0].texts_to_sequences(input_prep)
  inp = pad_sequences(inp, maxlen=lengths_input[0], padding='post', truncating='post')
  prediction = models[0].predict(inp)

  max_pred = max(prediction[0])
  for i, x in enumerate(prediction[0]):
    if x == max_pred:
      #print(x)
      prediction[0][i] = 1
    else:
      prediction[0][i]=0
  prediction_inverse_transformed = ohe.inverse_transform(prediction)
  #print('Predicted category is: ', prediction_inverse_transformed[0])
  var = prediction_inverse_transformed[0]
  if max_pred <= 0.28:
    output = 'Sorry, I did not understand that.'
    var = ''
  elif  sum(inp[0]) == 0:
    output = 'Hello, my friend. Unfortunately, I did not really understand that.'
  elif var == 'Beratung':
    output = '''Suchst du Informationen zur Beratungsangelegenheiten? \n
    Zu folgenden Themen konnten wir Informationen finden: 
    Zentrale Studienberatung, Nachhilfe und psychische Gesundheit: https://www.hs-aalen.de/de/facilities/11
    Psychosoziale Beratungsstelle: https://studierendenwerk-ulm.de/beratung-betreuung/psychosoziale-beratung/
    Gleichstellung, Chancengleichheit, Behinderung, Diversity sowie Hilfe bei Diskriminierung oder sexueller Belästigung: https://www.hs-aalen.de/de/facilities/219
    '''
  elif var == 'Bibliothek':
    inp_feel = tokenizers[1].texts_to_sequences(input_prep)
    inp_feel = pad_sequences(inp_feel, maxlen=lengths_input[1], padding='post', truncating='post')
    prediction = models[1].predict(inp_feel)
    max_pred = max(prediction[0])
    for i, x in enumerate(prediction[0]):
      if x == max_pred:
        prediction[0][i] = 1
      else:
        prediction[0][i]=0
    prediction_inverse_transformed = ohe2.inverse_transform(prediction)
    var_feeling = prediction_inverse_transformed[0]

    if max_pred <= 0.28:
      output = 'Sorry, I did not understand that.'
    elif var_feeling == 'Öffnungszeiten':
      output = 'Öffnungszeiten sind xyz...'
    elif var_feeling == 'LP_Reservieren':
      output = 'Hier reservierst du...'
    elif var_feeling == 'Bücher_suchen':
      output = 'Hier kannst du bücher suchen'
    elif max_pred > 0.28:
      output = '''Suchst du Informationen zur Bibliothek?\n
      Zu folgenden Themen konnten wir Informationen finden:
      Öffnungszeiten: https://www.hs-aalen.de/de/pages/bibliothek_oeffnungszeiten
      Bücher finden: https://www.hs-aalen.de/de/pages/bibliothek_suchenundfinden
      Reservierung Lernplatz: https://affluences.com/hochschule-aalen/bibliothek
      Publizieren und Open Access: https://www.hs-aalen.de/de/pages/bibliothek_publizieren-und-open-access
      Weitere Informationen zur Bibliothek könnt ihr hier finden: https://www.hs-aalen.de/de/facilities/3'''

  elif var == 'Bewerbung':
    output = '''Suchst du Informationen zur Bewerbung? \n
    Hier kannst du Infos zu der Bewerbung sowohl im Bachelor als auch im Master finden:
    https://www.hs-aalen.de/pages/bewerben
    '''
  elif var == 'Studentisches Leben':
    output = '''Hast du Fragen zum studentischen Leben hier in Aalen?
    Zu Folgenden Bereichen konnten Informationen gefunden werden:
    Wohnen, Mensa, Mobilität, Freizeit & Kultur, Hochschulleben, Hochschulsport, Lernräume, Lehrpreis, Karriereportal
    Alle Infos findest du hier: https://www.hs-aalen.de/de/facilities/63'''
  elif var == 'Studienangebot':
    output = 'Studienangebot'

  session['last_message'] = var

  var_string_prep = output
  var_string = str(var_string_prep)
  return var_string
  
 
