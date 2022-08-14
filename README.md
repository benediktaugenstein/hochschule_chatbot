# hochschule_chatbot

## Erklärung der Struktur des Repositorys

### Ordner
data: Datensätze zum Trainieren der Modelle  
models: TensorFlow-Modelle (Künstliche Neuronale Netze) zum Verarbeiten der Nutzereingaben  
templates: HTML-template zum Anzeigen der Web-App  
training: Skript (training_script.py), welches für das Trainieren der Modelle verwendet wurde  

### Dateien
Procfile: Festlegung des Python-Skripts, welches innerhalb der Flask Web-App ausgeführt werden soll  
main.py: Anzeigen der Web-App, Abfragen der Nutzereingaben sowie Anzeigen der Ergebnisse unter Verwendung des HTML-templates  
myfuncs.py: Funktion zur Korrektur bei Rechtschreibfehlern innerhalb der Nutzereingabe sowie Ermittlung der Antwort des Chatbots durch Analyse der Nutzereingabe  
requirements.txt: Erforderliche Softwarebibliotheken  
runtime.txt: Festlegen der Python-Version  

