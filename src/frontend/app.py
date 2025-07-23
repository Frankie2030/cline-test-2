import streamlit as st
import requests
from datetime import datetime

# Backend API base URL
BACKEND_URL = "http://127.0.0.1:8000"

# Initialize session state
if "token" not in st.session_state:
    st.session_state.token = None
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "username" not in st.session_state:
    st.session_state.username = None

def register_user(username, password):
    print(f"Attempting to register at {BACKEND_URL}/register")  # Debug
    try:
        response = requests.post(
            f"{BACKEND_URL}/register",
            json={"username": username, "password": password},
            timeout=5
        )
        print(f"Response status: {response.status_code}")  # Debug
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")  # Debug
        raise

def login_user(username, password):
    form_data = {"username": username, "password": password}
    response = requests.post(
        f"{BACKEND_URL}/login",
        data=form_data
    )
    return response.json()

def logout_user():
    st.session_state.token = None
    st.session_state.username = None
    st.session_state.conversation = []

def display_login():
    st.title("Chatbot Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            try:
                response = login_user(username, password)
                st.session_state.token = response.get("access_token")
                st.session_state.username = username
                st.success("Logged in successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {str(e)}")
    
    with col2:
        if st.button("Register"):
            try:
                response = register_user(username, password)
                if response and "message" in response:
                    st.success(response.get("message", "Registration successful!"))
                else:
                    st.error("Received invalid response from server")
            except requests.exceptions.JSONDecodeError:
                st.error("Server returned invalid response format")
            except requests.exceptions.RequestException as e:
                st.error(f"Network error: {str(e)}")
            except Exception as e:
                st.error(f"Registration failed: {str(e)}")

def display_chat():
    st.title(f"Chatbot - Welcome {st.session_state.username}")
    
    # Display chat messages
    for message in st.session_state.conversation:
        with st.chat_message(message["sender"]):
            st.write(f"{message['timestamp'].strftime('%H:%M:%S')}: {message['text']}")
    
    # Chat input
    if prompt := st.chat_input("Type your message"):
        # Add user message to conversation
        st.session_state.conversation.append({
            "sender": "user",
            "text": prompt,
            "timestamp": datetime.now()
        })
        
        # Call the backend chat endpoint
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        data = {"text": prompt}
        try:
            response = requests.post(f"{BACKEND_URL}/chat", json=data, headers=headers)
            if response.status_code == 200:
                bot_response = response.json()["response"]
            else:
                bot_response = f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            bot_response = f"Error: {str(e)}"
        
        # Add bot response to conversation
        st.session_state.conversation.append({
            "sender": "bot",
            "text": bot_response,
            "timestamp": datetime.now()
        })
        st.rerun()
    
    if st.button("Logout"):
        logout_user()
        st.rerun()

# Main app logic
if st.session_state.token:
    display_chat()
else:
    display_login()
