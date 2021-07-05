# Fancy Flashcards Bot

Der Fancy Flashcards Bot ist ein in Python implementierter Chatbot. Der Chatbot hilft beim Lernen. Der Bot basiert auf den [Fancy Flashcards](https://github.com/fancy-flashcard/ffc). Diese Idee wurde nun in einen Telegram Bot integriert. Der Bot verwendet die verfügbaren Decks der Fancy Flashcards. Einen genauen Überblick über die enthaltenen Decks im json ist [hier](https://github.com/fancy-flashcard/deck-collection/tree/main/wirtschaftsinformatik) zu finden.
Einen leichter zu lesenden Überblick gibt es [hier](https://github.com/michael-spengler/DHBW-Learning-Apps/blob/main/training-data.md).

Es können Fragen an den Bot gesendet werden. Die gesendete Frage wird mit den in den Decks enthaltenen Fragen verglichen. Die am besten passende Frage wird ausgegeben und beantwortet. 
Außerdem kann mit Hilfe des Bots gelernt werden. Dafür wird zunächst das gewünschte Deck gewählt. Anschließen stellt der Bot eine Frage. Die gegebene Antwort des Users wird überprüft. Der Bot gibt eine Rückmeldung ob die Antwort richtig ist oder nicht. Weiterhin gibt der Bot die Musterlösung zurück.
Ein detailierte Beschreibung der Funktionsweise gibt es unter [Funktionsweise des Botes](Funktionsweise-des-Botes).

## Funktionsweise des Bots

Folgendes kann eingeben werde um mit dem Bot zu kommunizieren.
Über /start können allgemeine Informationen über den Bot erlangt werden. Mit /help werden die Verfügbaren Funktionen erläutert. 
Mit /lernen kann gelernt werden. Als erstes wird gefragt welches Deck gelernt werden soll. Über die automatisch erscheinenden Buttons kann das gewünschte Deck ganz einfach ausgewählt werden. Im Anschluss stellt der Bot eine zufällige Frage aus dem gewählten Deck. Diese Frage kann nun beantwortet werden.

Im nächsten Schritt gibt der Bot eine Rückmeldung ob die Antwort richitg ist oder nicht und wie die Musterlösung aussieht. Außerdem wird gefragt, ob weiter gelernt werden soll, aufgehört werden soll oder das Deck gewechselt werden. Hier kann wieder über die Buttons geantwortet werden. 

Wenn eine Frage zu Inhalten der Decks besteht, kann die Frage eingetippt werden. Sollte sich der Bot nicht sicher sein welche Frage gemeint ist, erscheinen Auswahlbuttons. Nach Auswahl der gewünschten Frage antwortet der Bot auf die gewählte Frage.

Außerdem kann ein Timer gestellt werden während gelernt wird. Der Timer basiert auf der Promodoro Technick. Über /timer kann der Timer gestartet werden. Es kann aus vordefinierten Timern gewählt werden oder einen eigenen Timer einstellen. Die Auswahlmöglichkeiten erscheinen über Buttons. Bei den vordefinierten Timern wurde eine Arbeitszeit von 25 min bzw. 50 min festgelegt. Darauf folgt eine Pause von 5 min bzw. 10 min. Dieser Zyklus wird 2 mal wiederholt. Beim Benutzerdefinierten Timer wird nach den jeweiligen Zeitintervallen und Wiederholungen gefragt. Hier wird mit der gewünschten Zahl geantwortet.

![alt text](https://github.com/LeaKleemann/Fancy_Flashcards_Bot_project/blob/main/Screenshot_start.png)


## Programmierung des Bots
Der Telegram Bot wurde mit Hilfe des Package Python Telegram Bot in Python progrmmiert. Die Kommunikation des Bots mit dem User basiert auf sogennanten Handlern. Dabei können unterschiedliche Handler unterschieden werden. In diesem Programm wurde der Conversation Handler, Command Handler, Callback Query Handler sowie der Message Handler verwendet. Mit Hilfe des Conversation Handler kann eine vordefinierte Konversation definiert werden. Der Command Handler ruft festgelegte Funktionen auf. Dafür muss der User seine Nachricht mit einem / vor dem Text beginnen z.B. "/start". Durch den Callback Query Handler kann Feedback vom User direkt verarbeitet werden und basierend auf der Eingabe des Users wird die Konversation fortgeführt. Jeglicher Text der vom User eingegeben wird, wird vom Message Handler abgefangen und weiterverarbeitet.

## Bot starten
Der Bot kann wie folgt gestartet werden.

1. Clonen des Repositories
2. Installieren der Requierments (siehe [Requirements](Requirements))
3. Ausführen von `main.py` (`py main.py`)

## Verwendete Modelle
@Lea, Tamara beschreiben wo welche Modelle verwendet wurden
question checker, sentence_transf, questiontfidt, check answer
- Sentence Transformer
- Tf-idf
- Naive Bayes

## Datenbank
@Lea Aufbau Datenbank was für eine Datenbank ist das?

### Auslesen der Files von GitHub
@Tamara

## Installieren der Requirements
Die Requirements können über `pip install -r requirements.txt` installiert werden.

### Requirements 
- NLTK
- Numpy
- Pandas
- Pathlib 2
- Dotenv
- Python Telegram Bot 
- Scikit Learn
- Sentence Transformer
- Spacy 
-  Spacy Language Model (de-core-nes-sm/ de-core-nes-lg)
- SQLAlchemy
- Torch


## Gruppenmitglieder
- Lea Kleemann
- Tamara Bucher
- Maria Eichenlaub

### Verteilung der Aufgaben:

- Lea: NLP - Überprüfung der Antwort 

- Tamara: NLP - Beantwortung von Fragen

- Maria: Entwicklung des Telegram Chatbots
