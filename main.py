import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from googleapiclient.discovery import build
import os
import datetime
# import wikipedia

newsApi = os.environ.get("NEWS_API_KEY")
weatherApi = os.environ.get("WEATHER_API_KEY")
youtubeApi = os.environ.get("YOUTUBE_API_KEY")


def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def processCommand(c):
    c_lower = c.lower()

    if "open" in c_lower:
        parts = c_lower.split(" ")
        if len(parts) >= 2:
            site = parts[1]
            webbrowser.open(f"https://{site}.com")
        else:
            speak("Please specify a website to open")

    elif c_lower.startswith("play"):
        song = c_lower.replace("play", "").strip()
        if song:
            try:
                youtube = build("youtube", "v3", developerKey=youtubeApi)
                request = youtube.search().list(q=song, part="snippet", maxResults=1, type="video")
                response = request.execute()
                if response["items"]:
                    videoId = response["items"][0]["id"]["videoId"]
                    link = f"https://www.youtube.com/watch?v={videoId}"
                    speak(f"Playing {song}")
                    webbrowser.open(link)
                else:
                    speak(f"Could not find {song} on YouTube")
            except Exception as e:
                print("YouTube error:", e)
                speak("Failed to search YouTube")
        else:
            speak("Please specify a song to play")

    elif "news" in c_lower:
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsApi}")
            if r.status_code == 200:
                data = r.json()
                titles = [article["title"] for article in data.get("articles", [])]
                if titles:
                    for title in titles:
                        speak(title)
                        print(title, "\n")
                else:
                    speak("No news articles found")
            else:
                speak("Could not fetch news, please try again later")
        except requests.RequestException as e:
            print("News fetch error:", e)
            speak("Failed to fetch news")

    elif "weather" in c_lower:
        # expects: "weather in London"
        parts = c_lower.split("in")
        if len(parts) >= 2:
            city = parts[1].strip()
            try:
                r = requests.get(
                    f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weatherApi}&units=metric"
                )
                if r.status_code == 200:
                    data = r.json()
                    temp = data["main"]["temp"]
                    desc = data["weather"][0]["description"]
                    result = f"Weather in {city}: {desc}, {temp} degrees Celsius"
                    speak(result)
                    print(result)
                else:
                    speak(f"Could not find weather for {city}")
            except requests.RequestException as e:
                print("Weather fetch error:", e)
                speak("Failed to fetch weather")
        else:
            speak("Please specify a city, for example: weather in Mumbai")

    # elif "wikipedia" in c_lower:
    #     # expects: "wikipedia Albert Einstein"
    #     query = c_lower.replace("wikipedia", "").strip()
    #     if query:
    #         try:
    #             summary = wikipedia.summary(query, sentences=2)
    #             speak(summary)
    #             print(summary)
    #         except wikipedia.exceptions.DisambiguationError:
    #             speak("Too many results, please be more specific")
    #         except wikipedia.exceptions.PageError:
    #             speak(f"No Wikipedia page found for {query}")
    #     else:
    #         speak("Please specify a topic to search on Wikipedia")

    elif "search" in c_lower:
        # expects: "search python tutorials"
        query = c_lower.replace("search", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"Searching Google for {query}")
        else:
            speak("Please specify what to search")

    elif "time" in c_lower:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
        print(f"Time: {now}")

    elif "date" in c_lower:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {today}")
        print(f"Date: {today}")

    elif "stop" in c_lower or "exit" in c_lower or "quit" in c_lower:
        speak("Goodbye!")
        exit(0)

    else:
        speak("Sorry, I didn't understand that command")


if __name__ == "__main__":
    speak("Initialising Jarvis...")

    while True:
        r = sr.Recognizer()
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = r.listen(source, timeout=3, phrase_time_limit=3)

            word = r.recognize_google(audio)

            if word.lower() == "jarvis":
                speak("Jarvis Active")
                print("Jarvis Active")
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=1)
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    command = r.recognize_google(audio)
                    processCommand(command)

        except sr.WaitTimeoutError:
            print("Listening timed out, try again...")
        except sr.UnknownValueError:
            speak("Could not understand audio")
        except sr.RequestError as e:
            print("API Error:", e)
        except Exception as e:
            print("Error:", e)
