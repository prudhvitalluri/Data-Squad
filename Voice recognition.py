from time import ctime

import webbrowser as wb
import time
import playsound
import os
import random
from gtts import gTTS

import speech_recognition as sr

r = sr.Recognizer()


def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            squad_speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            squad_speak('unknown Value')
        except sr.RequestError:
            squad_speak('Speech service is down')
        return voice_data


def squad_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 1000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)


def respond(voice_data):
    if 'what is your name' in voice_data:
        squad_speak('squad_speak')
    if 'what time is it' in voice_data:
        squad_speak(ctime())
    if 'search' in voice_data:
        search = record_audio('what do you want to search for')
        url = 'https://google.com/search?q=' + search
        wb.get().open(url)
        squad_speak('Here is what i found ' + search)
    if "can you search for location" in voice_data:
        search = record_audio('what do you want to search for')
        url = 'https://www.google.co.in/maps?q=' + search + '/&amd'
        wb.get().open(url)
        squad_speak('Here is what i found ' + search)
    if 'exit' in voice_data:
        exit()


time.sleep(2)
squad_speak('How can I Help you?')
while 1:
    voice_data = record_audio()
    respond(voice_data)