import datetime
import os
import re
import sys
import webbrowser
import pywhatkit as kit
import pyttsx3
import speech_recognition as sr
import wikipedia
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')  # getting details of current voice
print(voices[0].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    # Without this command, speech will not be audible to us.
    engine.runAndWait()


def wishme():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    # male= Mimir, female=Athena,Minerva
    speak("Hello sir, I am Mimir. How can I assist you?")


def setReminder():
    speak("What should I remind you about?")
    reminder = takeCommand().lower()

    if reminder != "none":
        speak("In how many seconds should I remind you?")
        seconds = takeCommand()

        try:
            seconds = int(re.findall(r'\d+', seconds)[0])
            speak(f"I will remind you about {reminder} in {seconds} seconds")
            time.sleep(seconds)
            speak(f"Reminder: {reminder}")
        except (ValueError, IndexError):
            speak("Sorry, I didn't catch that. Please provide a valid number of seconds.")
    else:
        speak("Sorry, I didn't catch that.")


def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        # Using google for voice recognition.
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")  # User query will be printed

    except Exception as e:
        # Say that again will be printed in case of improper voice
        print("Say that again please...")
        return "None"  # None string will be returned
    return query


if __name__ == "__main__":
    wishme()
    while True:
        # if 1:
        query = takeCommand().lower()  # Converting user query into lower case

        # Logic for executing tasks based on query
        if 'wikipedia' in query:  # if wikipedia found in the query then this block will be executed
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'play music' in query:
            music_dir = 'D:\\music\\temp_songs'
            songs = os.listdir(music_dir)
            print(songs)
            if len(songs) > 0:
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                speak("No music files found in directory")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Sir, the time is {strTime}")

        elif 'open website' in query:
            speak("Which website would you like to open?")
            website = takeCommand().lower()
            if website != "none":
                webbrowser.open(f"https://{website}.com")
            else:
                speak("Sorry, I didn't catch that")

        elif 'search' in query:
            speak("What would you like me to search for?")
            search = takeCommand().lower()
            if search != "none":
                webbrowser.open(f"https://www.google.com/search?q={search}")
            else:
                speak("Sorry, I didn't catch that")

        elif 'calculate' in query:
            speak("What would you like me to calculate?")
            expression = takeCommand().lower()
            try:
                result = str(eval(expression))
                speak(f"The result of {expression} is {result}")
            except:
                speak("Sorry, I couldn't calculate that.")

        elif 'play music on youtube' in query:
            speak("What song would you like me to play?")
            song = takeCommand().lower()

            if song != "none":
                speak(f"Playing {song} on YouTube")
                kit.playonyt(song)
            else:
                speak("Sorry, I didn't catch that")

        elif 'reminder' in query:
            setReminder()

        elif 'quit' in query or 'exit' in query or 'close' in query:
            speak("Thank you for using Mimir Sir.")
            sys.exit()

        else:
            speak("Sorry, I didn't understand that command. Please try again.")
