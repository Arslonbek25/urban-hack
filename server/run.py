from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


from app import app

if __name__ == "__main__":
    app.run(port=8000, debug=True)
