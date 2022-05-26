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
    output = 'Entschuldigung, das habe ich nicht verstanden.'
    var = ''
  elif  sum(inp[0]) == 0:
    output = 'Tut mir leid, das sagt mir leider nichts.'
  elif var == 'Beratung':
    output = '''Suchst du Informationen zur Beratungsangelegenheiten?<br>
    Zu folgenden Themen konnten wir Informationen finden:<br>
    <a target="_blank" href="https://www.hs-aalen.de/de/facilities/11">Zentrale Studienberatung, Nachhilfe und psychische Gesundheit</a><br>
    <a target="_blank" href="https://studierendenwerk-ulm.de/beratung-betreuung/psychosoziale-beratung/">Psychosoziale Beratungsstelle</a><br>
    <a target="_blank" href="https://www.hs-aalen.de/de/facilities/219">Gleichstellung, Chancengleichheit, Behinderung, Diversity sowie Hilfe bei Diskriminierung oder sexueller Belästigung</a>
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

    if max_pred <= 0.28 or var_feeling == 'Sonstiges':
      output = '''Suchst du Informationen zur Bibliothek?<br>
      Zu folgenden Themen konnten wir Informationen finden:<br>
      <a target="_blank" href="https://www.hs-aalen.de/de/pages/bibliothek_oeffnungszeiten">Öffnungszeiten</a><br>
      <a target="_blank" href="https://www.hs-aalen.de/de/pages/bibliothek_suchenundfinden">Büchersuche</a><br>
      <a target="_blank" href="https://affluences.com/hochschule-aalen/bibliothek">Lernplatzreservierung</a><br>
      <a target="_blank" href="https://www.hs-aalen.de/de/pages/bibliothek_publizieren-und-open-access">Publizieren und Open Access</a><br>
      Weitere Informationen zur Bibliothek kannst du <a target="_blank" href="https://www.hs-aalen.de/de/facilities/3">hier</a> finden.'''
    elif var_feeling == 'Öffnungszeiten':
      output = '''Öffnungszeiten der Bibliothek:<br>
      Mo-Fr: 8-20 Uhr<br>
      Sa: 9-16 Uhr<br>
    Nicht das, was du gesucht hast?<br>
    <a target="_blank" href="https://www.hs-aalen.de/de/facilities/3">Hier</a> gibt es noch weitere Infos zur Bibliothek, ansonsten kannst du deine 
    Nachricht anpassen und nochmal eingeben.'''
    elif var_feeling == 'LP_reservieren':
      output = '''Hier kannst du dir einen Lernplatz reservieren: <a target="_blank" href="https://affluences.com/hochschule-aalen/bibliothek">Lernplatzreservierung</a><br>
      Nicht das, was du gesucht hast?<br>
      <a target="_blank" href="https://www.hs-aalen.de/de/facilities/3">Hier</a> gibt es noch weitere Infos zur Bibliothek, ansonsten kannst du deine 
      Nachricht anpassen und nochmal eingeben.'''
    elif var_feeling == 'suchen_ausleihen':
      output = '''Hier kannst du Bücher und Dokumente der Bibliothek durchsuchen: <a target="_blank" href="https://www.hs-aalen.de/de/pages/bibliothek_suchenundfinden">Büchersuche</a><br>
      Informationen zum Ausleihen findest du <a target="_blank" href="https://www.hs-aalen.de/de/pages/bibliothek_ausleihen-und-bestellen">hier</a>.
      Nicht das, was du gesucht hast?<br>
      <a target="_blank" href="https://www.hs-aalen.de/de/facilities/3">Hier</a> gibt es noch weitere Infos zur Bibliothek, ansonsten kannst du deine 
      Nachricht anpassen und nochmal eingeben.'''

  elif var == 'Bewerbung':
    output = '''Suchst du Informationen zur Bewerbung?<br>
    Hier kannst du Infos zu der Bewerbung sowohl im Bachelor als auch im Master finden:<br>
    <a target="_blank" href="https://www.hs-aalen.de/pages/bewerben">https://www.hs-aalen.de/pages/bewerben</a>'''
  elif var == 'Studentisches Leben':
    output = '''Hast du Fragen zum studentischen Leben hier in Aalen?<br>
    Zu Folgenden Bereichen konnten Informationen gefunden werden:<br>
    Wohnen, Mensa, Mobilität, Freizeit & Kultur, Hochschulleben, Hochschulsport, Lernräume, Lehrpreis, Karriereportal<br>
    Alle Infos findest du hier: <a target="_blank" href="https://www.hs-aalen.de/de/facilities/63">https://www.hs-aalen.de/de/facilities/63</a>'''
  elif var == 'Studienangebot':
    output = '''Hast du Fragen zum Studienangebot an der Hochschule Aalen?<br>
    Alle Infos findest du hier: <a target="_blank" href="https://studienangebot.hs-aalen.de/index.html">https://studienangebot.hs-aalen.de/index.html</a>'''
  elif var == 'Studieren':
    output = '''Hast du Fragen zum Studium an der Hochschule Aalen?<br>
    Zu folgenden Themen konnten wir Informationen finden:<br>
    <a target="_blank" href="https://www.hs-aalen.de/de/facilities/174">Studentische Abteilung</a><br>
    <a target="_blank" href="https://www.hs-aalen.de/de/facilities/190">Studien- und Prüfungsordnungen/Satzungen</a><br>
    <a target="_blank" href="https://www.hs-aalen.de/pages/raummanagement_vorlesungsplan">Vorlesungsplan/Raummanagement</a><br>
    <a target="_blank" href="https://www.hs-aalen.de/pages/studentische-abteilung_0_informationen-fuer-studienanfaenger">Informationen für Erstsemester</a>'''

  session['last_message'] = var

  var_string_prep = output
  var_string = str(var_string_prep)
  return var_string
  
 
