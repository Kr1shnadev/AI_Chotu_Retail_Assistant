import streamlit as st
import speech_recognition as sr
import pyaudio

def capture_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        st.write("Recognizing...")
        user_input = r.recognize_google(audio, language='en-IN')
        st.success(f"You said: {user_input}")
        return user_input
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")
    return None

# Streamlit app interface
st.title("Speech Recognition App")

st.write("Click the button below and speak into your microphone.")
if st.button("Start Listening"):
    capture_voice_input()
