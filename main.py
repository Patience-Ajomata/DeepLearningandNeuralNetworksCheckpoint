# Import necessary packages
import nltk
from nltk.chat import Chat, reflections
import streamlit as st
import speech_recognition as sr

# Load the text file and preprocess the data
with open('historyoftomjones.txt', 'r', encoding='utf-8') as f:
    data = f.read().replace('\n', ' ')

# Preprocess the data using the chatbot algorithm
nltk.download('punkt', quiet=True)
sentences = nltk.sent_tokenize(data)
words = nltk.word_tokenize(data)

# Define a function to transcribe speech into text
def transcribe_speech():
    # Initialize the speech recognition object
    r = sr.Recognizer()

    # Listen for speech input
    with sr.Microphone() as source:
        audio_text = r.listen(source)

    # Recognize the speech and return the transcribed text
    try:
        recognized_text = r.recognize_google(audio_text)
        return recognized_text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print("Error occurred in connecting to the API. Check your internet connection. Error: ", e)

def chatbot(user_input):
    if isinstance(user_input, str):
        # User provided text input
        response = get_bot_response(user_input)
    elif isinstance(user_input, sr.AudioData):
        # User provided speech input
        text = transcribe_speech(user_input)
        response = get_bot_response(text)
    else:
        raise TypeError("Invalid input type. Input must be either string or speech_recognition.AudioData.")
    return response
# Create the Streamlit app
st.title("Chatbot")

# Add a text input field
user_input = st.text_area("Enter text or press the microphone button to speak")

# Add a microphone button for speech input
if st.button("Record"):
    user_input = transcribe_speech()

# Get the chatbot response
if st.button("Get response"):
    if user_input:
        response = chatbot(user_input)
        st.write(response)
