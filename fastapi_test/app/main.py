from lucy import Lucy
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return "Hello, World!"

@app.post('/chat')
def chat(message:str):
    """basic chat endpoint"""
    lucy = Lucy()

    return lucy.turn(message)
