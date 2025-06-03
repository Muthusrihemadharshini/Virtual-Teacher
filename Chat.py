# chatbot.py
import pickle
import requests
from langchain_groq import ChatGroq
import openai
from PIL import Image
from io import BytesIO

# --- Load ChatGroq Model ---
try:
    with open('chatgroq_config.pkl', 'rb') as f:
        model_config = pickle.load(f)
except Exception as e:
    print(f"Error loading chatbot configuration: {e}")
    exit()

chatbot_model = ChatGroq(
    temperature=model_config["temperature"],
    groq_api_key=model_config["groq_api_key"],
    model_name=model_config["model_name"]
)

# --- OpenAI API Key for Image Generation ---
openai.api_key = "  # Replace with your API key"

# Function to Get Chatbot Response
def get_chatbot_response(user_input):
    try:
        response = chatbot_model.invoke(user_input)
        return response.content
    except Exception as e:
        return f"Error generating response: {e}"

# Function to Generate Image Using DALL·E API
def generate_image(prompt):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        return f"Error generating image: {e}"

# --- Chatbot Interface ---
if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        # Get Text Response
        text_response = get_chatbot_response(user_input)
        print(f"\nChatbot: {text_response}")
        
        # Get Image Response
        image_url = generate_image(user_input)
        if "Error" not in image_url:
            print(f"\nImage generated: {image_url}")
        else:
            print(f"\n{image_url}")

