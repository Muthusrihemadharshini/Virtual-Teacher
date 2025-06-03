import streamlit as st
from PIL import Image
import time
from chatbot import get_chatbot_response  # Ensure chatbot.py exists with this function

# Set page configuration (must be at the top)
st.set_page_config(
    page_title="Virtual Teacher for Kids",
    page_icon="🧸",
    layout="centered"
)

# Add session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header Section
st.title("🎨 Virtual Teacher for Children (Ages 4 to 8)")
st.subheader("Learn, Play, and Explore with AI!")

# Add an image (uncomment if you have the file)
image = Image.open("teacher.jpg")  
st.image(image, caption='Welcome to Your Virtual Classroom', use_container_width=True)

# Welcome message with animation
with st.spinner('Loading classroom...'):
    time.sleep(2)
st.success("Ready to start learning!")

# Sidebar for Navigation
st.sidebar.title("📚 Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Start Lesson", "AI Teacher", "Choose Dataset"])

# Main Content Based on Selection
if page == "Home":
    st.write("### 👋 Welcome to the Virtual Teacher Platform!")
    st.write("Children can explore subjects through AI-generated lessons tailored for their age.")
    st.info("Use the sidebar to navigate.")

elif page == "Start Lesson":
    st.write("### 📖 Let's Begin the Lesson!")
    subject = st.selectbox("Choose a Subject:", ["Math", "Science", "Story Time", "Art"])
    if st.button("Start!"):
        st.success(f"Starting {subject} lesson... Have fun learning!")

elif page == "AI Teacher":
    st.write("### 🤖 Chat with Your AI Teacher")
    
    # Display previous chat messages
    for message in st.session_state.messages:
        st.write(message)

    # Chat input
    user_input = st.text_input("You:", "")

    if user_input:
        # Get chatbot response
        response = get_chatbot_response(user_input)
        
        # Add user and bot messages to session state
        st.session_state.messages.append(f"**You:** {user_input}")
        st.session_state.messages.append(f"**AI Teacher:** {response}")

        # Display current response
        st.write(f"**AI Teacher:** {response}")

elif page == "Choose Dataset":
    st.write("### 📊 Choose Your Learning Dataset")
    dataset = st.file_uploader("Upload a dataset (CSV, JSON, etc.):")
    if dataset is not None:
        st.success(f"Dataset '{dataset.name}' uploaded successfully!")
    else:
        st.warning("Please upload a dataset to proceed.")

# Footer
st.markdown("---")
st.caption("👩‍🏫 Created with ❤️ by MSHD")
