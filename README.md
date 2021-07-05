# Fancy Flashcards Bot

Der Fancy Flashcards Bot ist ein in Python implementierter Chatbot. Der Chatbot hilft beim Lernen. Der Bot verwendet die verfügbaren Decks der Fancy Flashcards. Einen genauen Überblick über die enthaltenen Decks im json ist [hier](https://github.com/fancy-flashcard/deck-collection/tree/main/wirtschaftsinformatik) zu finden.
Einen leichter zu lesenden Überblick gibt es [hier](https://github.com/michael-spengler/DHBW-Learning-Apps/blob/main/training-data.md).

Es können Fragen an den Bot gesendet werden. Die gesendete Frage wird mit den in den Decks enthaltenen Fragen verglichen. Die am besten passende Frage wird ausgegeben und beantwortet. 
Außerdem kann mit Hilfe des Bots gelernt werden. Dafür wird zunächst das gewünschte Deck gewählt. Anschließen stellt der Bot eine Frage. Die gegebene Antwort des Users wird überprüft. Der Bot gibt eine Rückmeldung ob die Antwort richtig ist oder nicht. Weiterhin gibt der Bot die Musterlösung zurück.
Ein detailierte Beschreibung der Funktionsweise gibt es unter [Funktionsweise des Botes](Funktionsweise-des-Botes).



## Funktionsweise des Bots

Folgendes kann eingeben werde um mit dem Bot zu kommunizieren.
Mit /lernen kann gelernt werden. Als erstes wird gefragt welches Deck gelernt werden soll. Über die automatisch erscheinenden Buttons kann das gewünschte Deck ganz einfach ausgewählt werden. Im Anschluss stellt der Bot eine zufällige Frage aus dem gewählten Deck. Diese Frage kann nun beantwortet werden.

WICHTIG: Wenn über Telegram Web gelernt wird, muss zunächst die Nachricht mit der Frage ausgewählt werden und reply gedrückt werden. Wird über die App gelernt wird automatisch auf die Nachricht mit der Frage geantwortet. Das ist wichtig, damit der Bot überprüfen kann, ob die Antwort richtig ist.

Im nächsten Schritt gibt der Bot eine Rückmeldung ob die Antwort richitg ist oder nicht und wie die Musterlösung aussieht. Außerdem wird gefragt, ob weiter gelernt werden soll, aufgehört werden soll oder das Deck gewechselt werden. Hier kann wieder über die Buttons geantwortet werden. Sollteten Inhalte der Frage vom Bot nicht verständlich sein, lösche das Antworten auf die letzte Nachricht und tippe die Frage ein. Der Bot antwortet auf die Frage.

Wenn eine Frage zu Inhalten der Decks besteht, kann die Frage eingetippt werden. Sollte sich der Bot nicht sicher sein welche Frage gemeint ist, erscheinen Auswahlbuttons. Nach Auswahl der gewünschten Frage antwortet der Bot auf die gewählte Frage.

Außerdem kann ein Timer gestellt werden während gelernt wird. Der Timer basiert auf der Promodoro Technick. Über /timer kann der Timer gestartet werden. Es kann aus vordefinierten Timern gewählt werden oder einen eigenen Timer einstellen. Die Auswahlmöglichkeiten erscheinen über Buttons. Bei den vordefinierten Timern wurde eine Arbeitszeit von 25 min bzw. 50 min festgelegt. Darauf folgt eine Pause von 5 min bzw. 10 min. Dieser Zyklus wird 2 mal wiederholt. Beim Benutzerdefinierten Timer wird nach den jeweiligen Zeitintervallen und Wiederholungen gefragt. Hier wird mit der gewünschten Zahl geantwortet.

## Datenbank

### Automatisches Auslesen der Files von GitHub

## Programmiersprache und Technolgien
- Python
- Python Telegram Bot API
- Spacy

## Verwendete Modelle
- Sentence Transformer
- Tf-idf
- Naive Bayes

## Requirements 
- Telegram Bot API
- numpy
- pandas
- pathlib2
- os
- timer
- dotenv
- threading
- sklearn
- torch
- sentence transformer
- sklearn
- sqlalchemy
- random
- 
## Bot starten

## Gruppenmitglieder
- Lea Kleemann
- Tamara Bucher
- Maria Eichenlaub

### Verteilung der Aufgaben:

- Lea: NLP - Überprüfung der Antwort 

- Tamara: NLP - Beantwortung von Fragen

- Maria: Entwicklung des Telegram Chatbots
