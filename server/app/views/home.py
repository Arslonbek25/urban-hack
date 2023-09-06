import os
import secrets
from http import HTTPStatus

from flask import request

from app import app


@app.get("/")
def home():
    return "hello"

@app.get("/chat/<int:id>")
def chat():
    return "Answer"


def allowed_file(filename):
    return filename.split(".")[-1] in ("png", "jpg", "jpeg")


def save_picture(file):
    random_hex = secrets.token_hex(8)
    filename = random_hex + os.path.splitext(file.filename)[1]
    path = os.path.join(app.root_path, "static", "x-rays", filename)
    file.save(path)
    return filename


@app.post("/upload_image")
def upload_picture():
    file = request.files.get("image")
    if file and allowed_file(file.filename):
        filename = save_picture(file)

        # old = os.path.join(app.root_path, "static", current_user.image_file)
        # if os.path.exists(old):
        #     os.remove(old)

        # current_user.image_file = filename
        # db.session.commit()
        return {"message": "File uploaded successfully"}

    return {"error": "Invalid file"}, HTTPStatus.BAD_REQUEST
