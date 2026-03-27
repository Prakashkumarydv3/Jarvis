import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests

engine = pyttsx3.init()
newsApi = "0f50457f4b0b4ae394b80448881f14b6"


def speak(text):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id) 
    engine.say(text)
    engine.runAndWait()
    
def processCommand(c):
    # print("in command",c)
    if("open" in c.lower()):
        webbrowser.open(f"https://{c.split(' ')[1]}.com")
    elif(c.lower().startswith("play")):
        song = c.lower().split(" ")[1]
        link = musicLibrary.songs[song]
        webbrowser.open(link)
    elif("news" in c.lower()):
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsApi}")
        data = r.json()
        titles = [article["title"] for article in data["articles"]]

        for title in titles:
            speak(title)
            print(title,"\n")
    # print(c)
    
# Initialize recognizer class (for recognizing the speech)
if __name__ == "__main__":
    speak("Initialising Julie...")
    

    while True:
        r = sr.Recognizer()
        
        print("Recognizing...")
        try:
            # with sr.Microphone() as source:
            #     print("Adjusting for ambient noise, please wait...")
            #     r.adjust_for_ambient_noise(source, duration=2) 
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=3, phrase_time_limit=3)
                # using google speech recognition
            word = r.recognize_google(audio)
            # speak(word)
            if(word.lower() == "jarvis"):
                
                speak("Active")
                print(word)
                with sr.Microphone() as source:
                    print("Jarvis Active")
                    speak("Jarvis Active")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        
        
        except sr.WaitTimeoutError:
            print("Listening timed out, try again...")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("API Error:", e)
        except Exception as e:
            print("Error:", e)
