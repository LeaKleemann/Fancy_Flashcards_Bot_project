from datetime import date, datetime
import time 
import questiontfidf as Q

def sample_responses(input_text):
    print("Sample responses", input_text)
    #user_message = str(input_text).lower()
    frage, wert=Q.question_distance(input_text)
    print("frage",frage)
    print("wert", wert)
    wert=''.join(str(wert))
    print("wertc", wert)
    


    # if user_message in ("hello", "hi", "hallo"):
    #     return "Hey! How is it going?"

    # if user_message in ("who are you", "who are you?", "wer bist du" "wer bist du?"):
    #     return "Ich bin ein Test Bot"

    # if user_message in ("time", "time?", "zeit", "zeit?", "datum", "datum?"):
    #     now = datetime.now()
    #     date_time=now.strftime("%d/%m/%y, %H:%M:%S")

    #     return str(date_time)

    # if user_message == "business intelligence":
    #    return "Du hast Business Intelligence gewählt"

    # if user_message in "unternehmensführung":
    #     return"Du hast Unternehmensführung gewählt"

    # if user_message == "wirtschaftsinformatik":
    #     return "Du hast Wirtschaftsinformatik gewählt"

    # if user_message == "bwl":
    #     return"Du hast BWL gewählt"

    # if user_message == "25:5 intervall":
    #     for i in range(1):
    #         t=25
    #         while t:
    #             mins = t // 60
    #             secs = t % 60
    #             timer = '{:02d}:{:02d}'.format(mins,secs)
    #             print(" " + timer, end="\r")
    #             time.sleep(1)
    #             t-=1
    #         print("Break Time!!")
    #         t=10
    #         while t:
    #             mins = t // 60
    #             secs = t % 60
    #             timer = '{:02d}:{:02d}'.format(mins,secs)
    #             print(" " + timer, end="\r")
    #             time.sleep(1)
    #             t-=1
    #         print("Work Time")
    #     return
            
    text=[frage, wert]
    print("text", text)
    return text
    # "I don't unsterand you."