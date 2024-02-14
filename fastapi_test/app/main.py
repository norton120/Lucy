from sid import Sid
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return "Hello, World!"

@app.post('/chat')
def chat(message:str):
    """basic chat endpoint"""
    sid = Sid()

    return sid.turn(message)
