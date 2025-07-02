import streamlit as st
import whisper
import os
import tempfile
from pydub import AudioSegment
import time

# Load Whisper model (GPU will be used automatically if available)
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

model = load_whisper_model()

st.set_page_config(page_title="PodNotes AI", layout="centered")
st.title("🎙️ PodNotes AI - Smart Podcast Transcriber")
st.write("Upload a podcast or speech `.mp3` or `.wav` file to generate a transcript.")

uploaded_file = st.file_uploader("Upload Audio File", type=["mp3", "wav"])

if uploaded_file is not None:
    with st.spinner("Processing audio..."):
        # Convert to WAV
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            audio = AudioSegment.from_file(uploaded_file)
            audio.export(temp_audio.name, format="wav")
            temp_audio_path = temp_audio.name

        # Transcribe
        result = model.transcribe(temp_audio_path, fp16=True)
        transcript = result["text"]

        st.subheader("📝 Full Transcript")
        st.text_area("Transcript", transcript, height=300)

        # Download transcript
        st.download_button("Download Transcript", transcript, file_name="transcript.txt")

        # Clean up
        time.sleep(1)
        try:
            os.unlink(temp_audio_path)
        except Exception as e:
            st.warning(f"Could not delete temp file: {e}")
