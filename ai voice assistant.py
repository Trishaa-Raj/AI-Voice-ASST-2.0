import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import webbrowser
import os
import pyjokes
import psutil
import pyautogui

def initialize_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 160)
    return engine

def talk(text, engine):
    engine.say(text)
    engine.runAndWait()

def take_command(listener, engine):
    for attempt in range(3):
        try:
            with sr.Microphone() as source:
                print("Listening...")
                listener.adjust_for_ambient_noise(source, duration=1)
                audio = listener.listen(source, timeout=10)
            print("Recognizing...")
            command = listener.recognize_google(audio).lower()
            print(f"User said: {command}")
            return command
        except sr.UnknownValueError:
            talk("I didn't catch that, please say it again.", engine)
        except sr.RequestError:
            talk("Speech service is unavailable. Retrying...", engine)
        except ConnectionResetError:
            talk("Network issue detected. Retrying...", engine)
    talk("I'm having trouble understanding you. Please try again later.", engine)
    return ""

def run_assistant(command, engine):
    if "play" in command:
        song = command.replace("play", "").strip()
        talk(f"Playing {song} on YouTube.", engine)
        pywhatkit.playonyt(song)
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        talk(f"The current time is {current_time}", engine)
    elif "who is" in command or "what is" in command:
        topic = command.replace("who is", "").replace("what is", "").strip()
        try:
            info = wikipedia.summary(topic, sentences=1)
            talk(info, engine)
        except:
            talk(f"Sorry, I couldn't find information on {topic}.", engine)
    elif "open" in command:
        website = command.replace("open", "").strip().lower()
        web_dict = {"google": "https://www.google.com", "facebook": "https://www.facebook.com", "youtube": "https://www.youtube.com"}
        if website in web_dict:
            webbrowser.open(web_dict[website])
        else:
            webbrowser.open(f"https://{website}.com")
        talk(f"Opening {website}", engine)
    elif "joke" in command:
        talk(pyjokes.get_joke(), engine)
    elif "search for" in command:
        query = command.replace("search for", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        talk(f"Here are the search results for {query}.", engine)
    elif "shut down" in command:
        talk("Shutting down your computer.", engine)
        os.system("shutdown /s /t 5")
    elif "restart" in command:
        talk("Restarting your computer.", engine)
        os.system("shutdown /r /t 5")
    elif "battery status" in command:
        battery = psutil.sensors_battery()
        talk(f"Your system battery is at {battery.percent} percent.", engine)
    elif "volume up" in command:
        pyautogui.press("volumeup")
        talk("Increasing volume.", engine)
    elif "volume down" in command:
        pyautogui.press("volumedown")
        talk("Decreasing volume.", engine)
    elif "exit" in command or "stop" in command:
        talk("Goodbye! Have a great day.", engine)
        exit()
    else:
        talk("I'm sorry, I didn't understand that. Can you repeat?", engine)

if __name__ == "__main__":
    listener = sr.Recognizer()
    engine = initialize_engine()
    talk("Hello! I am your AI assistant.", engine)
    while True:
        command = take_command(listener, engine)
        if command:
            run_assistant(command, engine)
