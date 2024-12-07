import threading
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import streamlit as st
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import Config, Server

# --- FastAPI Backend ---
app = FastAPI()

# Add CORS to allow Streamlit to interact with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify frontend URL)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the login request model
class LoginRequest(BaseModel):
    username: str
    password: str

# Define the login route
@app.post("/login")
async def login(request: LoginRequest):
    if request.username == "admin" and request.password == "password123":
        return {"status": "success", "message": "Login successful"}
    return {"status": "error", "message": "Invalid credentials"}


# Function to run FastAPI in a separate thread
def run_backend():
    config = Config(app=app, host="0.0.0.0", port=8000, log_level="info")
    server = Server(config)
    server.run()


# Start FastAPI in a background thread
thread = threading.Thread(target=run_backend, daemon=True)
thread.start()

# --- Streamlit Frontend ---
st.title("Streamlit + FastAPI Integration")
st.write("Interact with the FastAPI backend through this Streamlit interface.")

# Login form
st.subheader("Login Form")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    # Send a POST request to the FastAPI backend
    try:
        response = requests.post(
            "http://localhost:8000/login",
            json={"username": username, "password": password},
        )
        result = response.json()
        if result["status"] == "success":
            st.success(result["message"])
        else:
            st.error(result["message"])
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")
