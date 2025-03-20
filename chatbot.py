import streamlit as st
import os
import time
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Set page config
st.set_page_config(page_title="OpenAI GPT Chatbot", layout="wide")
st.title("OpenAI GPT Chatbot")
st.write("Welcome to the OpenAI GPT Chatbot! Ask me anything.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful, creative, clever, and friendly AI assistant."}
    ]

# Function to generate response using OpenAI API
def generate_response(messages, model="gpt-3.5-turbo", temperature=0.7, max_tokens=150):
    start_time = time.time()
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        generation_time = time.time() - start_time
        return response.choices[0].message.content, generation_time
    except Exception as e:
        return f"Error: {str(e)}", time.time() - start_time

# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":  # Don't display system messages
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Sidebar for model parameters
with st.sidebar:
    st.header("Model Parameters")
    
    model = st.selectbox(
        "Model",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        index=0,
        help="Select the OpenAI model to use"
    )
    
    temperature = st.slider(
        "Temperature", 
        min_value=0.0, 
        max_value=2.0, 
        value=0.7, 
        step=0.1,
        help="Higher values make output more random, lower values more deterministic"
    )
    
    max_tokens = st.slider(
        "Max Tokens", 
        min_value=50, 
        max_value=4000, 
        value=500, 
        step=50,
        help="Maximum length of generated response"
    )
    
    st.header("Model Information")
    st.info(f"Using {model} from OpenAI API. This requires a valid API key set in your environment variables.")
    
    st.write("**What can this chatbot do?**")
    st.write("- Answer general knowledge questions")
    st.write("- Provide creative responses")
    st.write("- Engage in casual conversation")
    st.write("- Generate text based on prompts")
    st.write("- Remember context from previous messages")

# User input
user_input = st.chat_input("Type your message here...")

# Process user input
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Generate response
            response, generation_time = generate_response(
                st.session_state.messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Display response
            st.markdown(response)
            st.caption(f"Response generated in {generation_time:.2f} seconds")
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Add a reset button
if st.button("Reset Conversation"):
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful, creative, clever, and friendly AI assistant."}
    ]
    st.experimental_rerun()