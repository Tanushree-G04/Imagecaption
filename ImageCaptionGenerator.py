# streamlit run ImageCaptionGenerator.py

import os
import pathlib

import filetype
import streamlit as st
from gtts import gTTS
from PIL import Image

from config import IMAGE_PATH
from model import image_caption_generator

FILE_PATH = pathlib.Path(__file__)

BASE_FILE = FILE_PATH.parent.absolute()

st.title("Image Caption Generator")

uploaded_file = st.file_uploader("Choose a file")
if (
    "uploaded_file" in st.session_state
    and st.session_state["uploaded_file"] is not None
):
    del st.session_state["uploaded_file"]
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    kind = filetype.guess(bytes_data)
    if "image" in kind.mime.lower():
        with open(IMAGE_PATH, "wb") as f:
            f.write(bytes_data)
    else:
        st.error("Please upload image file ...", icon="🚨")

text = image_caption_generator(IMAGE_PATH)
if st.button("Generate Image Caption", type="primary"):
    st.image(IMAGE_PATH)
    st.title(text.title())
    st.session_state["uploaded_file"] = None

if text.strip() != "":
    text = image_caption_generator(IMAGE_PATH)
    st.write("Converting text to speech...")
    tts = gTTS(text)

    # Save the audio file
    tts.save("output.mp3")

    # Provide a way to play the audio file in Streamlit
    audio_file = open("output.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
else:
    st.write("No text found in the image.")


# Clean up
if os.path.exists("audio.mp3"):
    os.remove("audio.mp3")
