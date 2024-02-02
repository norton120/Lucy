from fastapi import FastAPI

app = fastapi.FastAPI()

@app.get('/')
def index():
    return "Hello, World!"