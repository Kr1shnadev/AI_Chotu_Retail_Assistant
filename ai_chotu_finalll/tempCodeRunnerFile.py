import os
import speech_recognition as sr
from gtts import gTTS
import playsound

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    filename = "temp.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something:")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def main():
    # Example of using text-to-speech
    text_to_speech("Hello! How can I assist you today?")
    
    # Example of using speech-to-text
    user_input = speech_to_text()
    if user_input:
        text_to_speech(f"You said: {user_input}")

if __name__ == "__main__":
    main()