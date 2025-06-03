import streamlit as st
from PIL import Image
import time
import speech_recognition as sr
import pyaudio
import wave
from chatbot import get_chatbot_response  # Ensure chatbot.py exists with this function
import random

# Set page configuration
st.set_page_config(
    page_title="Virtual Teacher for Kids",
    page_icon="🧸",
    layout="centered"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

def record_audio(filename="audio.wav", duration=5, rate=44100, channels=1):
    """Records audio and saves it as a WAV file."""
    chunk = 1024
    format = pyaudio.paInt16
    audio = pyaudio.PyAudio()
    
    stream = audio.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    st.write("🎙️ Recording... Speak now!")
    
    frames = []
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
    
    return filename

def transcribe_audio(file_path="audio.wav"):
    """Transcribes recorded audio to text using Google Speech Recognition."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except Exception:
        return "Could not recognize your voice. Try again."

# Header Section
st.title("🎨 Virtual Teacher for Children (Ages 4 to 8)")
st.subheader("Learn, Play, and Explore with AI!")

# Add an image
image = Image.open("teacher.jpg")  
st.image(image, caption='Welcome to Your Virtual Classroom', use_container_width=True)

# Sidebar for Navigation
st.sidebar.title("📚 Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Start Lesson", "AI Teacher", "Mini-Games & Quizzes", "Creative Corner", "Interactive Story Mode", "Voice Chat"])

# Home Page
if page == "Home":
    st.write("### 👋 Welcome to the Virtual Teacher Platform!")
    st.write("Children can explore subjects through AI-generated lessons tailored for their age.")

# Start Lesson
elif page == "Start Lesson":
    subject = st.selectbox("Choose a Subject:", ["Math", "Science", "Social science ", "English"])
    if st.button("Start!"):
        st.success(f"Starting {subject} lesson... Have fun learning!")

# AI Teacher Chatbot
elif page == "AI Teacher":
    st.write("### 🤖 Chat with Your AI Teacher")
    for message in st.session_state.messages:
        st.write(message)
    user_input = st.text_input("You:", "")
    if user_input:
        response = get_chatbot_response(user_input)
        st.session_state.messages.append(f"**You:** {user_input}")
        st.session_state.messages.append(f"**AI Teacher:** {response}")
        st.write(f"**AI Teacher:** {response}")
        st.write("click left and select read aloud to have voice over ")

# Mini-Games & Quizzes
elif page == "Mini-Games & Quizzes":
    quiz_question = {
        "Math": ["What is 2+2?", "What comes after 6?", "How many sides does a square have?"],
        "Science": ["What do plants need to grow?", "What is the color of the sky?", "Which animal says 'Meow'?"],
    }
    subject = st.selectbox("Choose a subject for a quiz:", list(quiz_question.keys()))
    question = random.choice(quiz_question[subject])
    st.write(f"**Question:** {question}")
    answer = st.text_input("Your Answer:")
    if answer:
        st.success("Great job! Keep learning!")

# Creative Corner
elif page == "Creative Corner":
    st.file_uploader("Upload your artwork (JPG, PNG, etc.):")
    st.success("Your artwork is amazing! Keep creating!")

# Interactive Story Mode
elif page == "Interactive Story Mode":
    story = {
        "Jungle Adventure": "You are in a deep jungle. Do you go left (towards a river) or right (towards a cave)?",
    }
    selected_story = st.selectbox("Pick a story:", list(story.keys()))
    st.write(story[selected_story])
    choice = st.radio("Make a choice:", ["Option 1", "Option 2"])
    if choice:
        st.success("Great choice! Your story continues...")

# Voice Chat
elif page == "Voice Chat":
    st.write("### 🎤 Talk to Your AI Teacher!")
    if st.button("Record Voice Message"):
        audio_file = record_audio()
        user_voice_input = transcribe_audio(audio_file)
        st.write(f"**You said:** {user_voice_input}")
        response = get_chatbot_response(user_voice_input)
        st.write(f"**AI Teacher:** {response}")

# Footer
st.markdown("---")
st.caption("👩‍🏫 Created with ❤️ by MSHD")
