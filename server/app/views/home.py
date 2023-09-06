from app import app, models

@app.get("/")
def home():
    return "hidfsd"