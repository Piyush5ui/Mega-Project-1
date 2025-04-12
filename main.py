import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "b40e955cc75c44549e9dea92f08e65d0"


def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
   tts = gTTS(text)
   tts.save('temp.mp3')

    # Initialize Pygame mixer
   pygame.mixer.init()

    # Load the MP3 file
   pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
   pygame.mixer.music.play()

    # Keep the program running until the music stops playing
   while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
   pygame.mixer.music.unload()
   os.remove("temp.mp3") 


def aiProcess(command):
   client = OpenAI(api_key="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",)

   completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
    {"role": "user", "content": "command"}
  ]
  )

   return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
      webbrowser.open("https://www.google.com")
    elif "open instagram" in c.lower():
      webbrowser.open("https://www.instagram.com")
    elif "open youtube" in c.lower():
      webbrowser.open("https://www.youtube.com")
    elif c.lower().startswith("play"):
       song = c.lower().split(" ")[1]
       link = musicLibrary.music[song]
       webbrowser.open(link)

    elif "news" in c.lower():
       r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
       if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])


    else:
       #Let openAI handel the request
       output = aiProcess(c)
       speak(output)

 
       
if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
        
        print("recognizing...")
        # recognize speech using Sphinx
        try:
            with sr.Microphone() as source:
             print("Listening....")
             audio = r.listen(source , timeout=2, phrase_time_limit=1)
             word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                #Listen for command
            with sr.Microphone() as source:
             print("Jarvis Active...")
             audio = r.listen(source)
            command = r.recognize_google(audio)


            processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))