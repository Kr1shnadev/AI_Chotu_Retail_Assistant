import streamlit as st
from groq import Groq
from dbtalk import fetch_and_query_product_data
from sqlquery import execute_sql_query
import speech_recognition as sr
from gtts import gTTS
import os
import uuid
import time
import pygame

# Function to convert text to speech and play it
def text_to_speech(text):
    # Only speak for casual conversations, not database-related responses
    if any(keyword in text.lower() for keyword in ["table", "database", "query", "column", "row"]):
        return  # Do nothing if the response is database-related

    tts = gTTS(text=text, lang='en')
    filename = f"temp_{uuid.uuid4()}.mp3"
    tts.save(filename)

    if os.path.exists(filename):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        finally:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            os.remove(filename)

# Function to capture voice input
def capture_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try: 
        st.write("Recognizing...")
        user_input = r.recognize_google(audio, language='en-in')
        st.write(f"You said: {user_input}")
        return user_input
    except Exception as e:
        st.write("Sorry, I could not understand the audio.")
        return None

# Function to handle user input
def handle_user_input(user_input, from_voice=False):
    # Initialize Groq client
    client = Groq(api_key="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")

    # Classify user intent
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{
            "role": "system",
            "content": "Classify the following user input into 'action' (for database actions like insert, add, delete) or 'inquiry' (for questions about the database). Give one-word reply."
        }, {
            "role": "user",
            "content": user_input
        }],
        temperature=0,
        max_tokens=10,
        top_p=1,
        stream=False,
        stop=None,
    )

    # Get the classification result
    intent = completion.choices[0].message.content.strip().lower()
    
    # If SQL operation, do not talk back
    if intent == "action":
        execute_sql_query(user_input)  # Execute SQL without speaking back
        return None  # Return nothing to prevent speech output for SQL actions

    # Handle based on intent
    if intent == "inquiry":
        return fetch_and_query_product_data(user_input)
    else:
        return "Unable to determine the intent. Please clarify your request."

# Function to create the Streamlit interface
def create_streamlit_interface():
    st.title("Product Database Query Interface")

    # User input options
    input_type = st.selectbox("Select Input Type", ["Text Input", "Voice Input"])

    if input_type == "Text Input":
        user_input = st.text_input("Enter your query:")
        if st.button("Submit"):
            if user_input:
                output = handle_user_input(user_input)
                if output:  # Only speak for non-SQL responses
                    st.write("Output:")
                    st.write(output)
                    text_to_speech(output)  # Add voice output for inquiries
                else:
                    st.write("SQL operation executed without vocal feedback.")
            else:
                st.write("Please enter a query.")
    elif input_type == "Voice Input":
        if st.button("Capture Voice Input"):
            user_input = capture_voice_input()
            if user_input:
                output = handle_user_input(user_input, from_voice=True)
                if output:  # Only speak for non-SQL responses
                    st.write("Output:")
                    st.write(output)
                    text_to_speech(output)  # Add voice output for inquiries
                else:
                    st.write("SQL operation executed without vocal feedback.")

# Run the Streamlit interface
if __name__ == "__main__":
    create_streamlit_interface()
