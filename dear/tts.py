import pyttsx3


def do_tts(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    