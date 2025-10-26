import streamlit as st
import requests
import sounddevice as sd
import wavio
import os
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = "sk-" #give your API key

# Initialize OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Record audio function
def record_audio(filename, duration, fs):
    st.write("Recording audio...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    wavio.write(filename, recording, fs, sampwidth=2)
    st.write(f"Audio recorded and saved as {filename}")

st.title("Voice to Image Generator")

if st.button("Click here to speak"):
    audio_filename = "input.wav"
    duration = 5  # seconds
    fs = 44100  # sample rate
    record_audio(audio_filename, duration, fs)

    # Convert audio to text using Whisper
    with open(audio_filename, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    text = transcript.text
    st.write("You said:", text)

    # Generate image using DALL·E
    response = client.images.generate(
        model="dall-e-2",
        prompt=text,
        size="1024x1024",
        n=1
    )
    image_url = response.data[0].url
    image_response = requests.get(image_url)

    # Save the image locally
    image_path = "generated_image.jpg"
    with open(image_path, "wb") as f:
        f.write(image_response.content)

    st.write("Generated Image:")
    st.image(image_path)
