# speech_recognition_app.py
# A Streamlit app for uploading audio files and transcribing them.
# This app supports multiple speech recognition APIs and languages.

import streamlit as st
import speech_recognition as sr
import os
import tempfile

# Initialize recognizer
recognizer = sr.Recognizer()

# Supported APIs
API_OPTIONS = {
    "Google Web Speech API": "google",
    "CMU Sphinx (Offline)": "sphinx"
}

# Supported Languages
LANGUAGES = {
    "English (US)": "en-US",
    "French": "fr-FR",
    "Spanish": "es-ES",
    "Swahili": "sw-KE",
}

# UI Title
st.title("Audio File Transcriber")
st.markdown("Upload a voice recording (`.wav`, `.mp3`, etc.) and transcribe it.")

# Choose API and language
api_choice = st.selectbox("Choose Speech Recognition API", list(API_OPTIONS.keys()))
language = st.selectbox("Choose Language", list(LANGUAGES.keys()))

# File uploader
uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "flac", "aiff", "aif"])

# Transcribe function
def transcribe_audio_file(file_path, api="google", language="en-US"):
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
            if api == "google":
                return recognizer.recognize_google(audio, language=language)
            elif api == "sphinx":
                return recognizer.recognize_sphinx(audio, language=language)
            else:
                return "Unsupported API selected."
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        return f"API error: {e}"
    except Exception as e:
        return f"Error: {str(e)}"

# Handle transcription
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.info("Transcribing audio...")
    result = transcribe_audio_file(tmp_path, api=API_OPTIONS[api_choice], language=LANGUAGES[language])
    st.text_area("Transcribed Text", value=result, height=200)

    if st.button("Save to transcription.txt"):
        with open("transcription.txt", "w", encoding="utf-8") as f:
            f.write(result)
        st.success("Saved to transcription.txt successfully!")
        
# This was Hectic        
# =============================================