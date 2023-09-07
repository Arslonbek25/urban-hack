import os
import secrets
from datetime import datetime, timedelta
from http import HTTPStatus

from flask import jsonify, request, session
from flask_login import current_user

from app import app
from app.extensions import db
from app.models import Chat, ImageMessage, TextMessage


@app.get("/")
def home():
    return "hello world"

@app.get("/chats")
def chats():
    return [c.dict for c in current_user.chats]


@app.post("/chat/<int:id>")
def chat(id):
    user_message = request.json.get("text", "")
    timestamp = datetime.utcnow()
    chat = Chat.query.get(id)
    if not chat:
        chat = Chat(user_id=current_user.id)
        db.session.add(chat)
        db.session.commit()

    user = TextMessage(
        chat_id=chat.id,
        text=user_message,
        sender="user",
        timestamp=timestamp,
    )
    db.session.add(user)

    bot_response = "Hello, this is a dummy response."
    bot_msg = TextMessage(
        chat_id=chat.id,
        text=bot_response,
        sender="bot",
        timestamp=timestamp + timedelta(seconds=1),
    )
    db.session.add(bot_msg)
    db.session.commit()

    return jsonify({"bot_response": bot_response, "chat_id": chat.id})


@app.get("/chat/<int:id>")
def chat_history(id):
    chat = Chat.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    messages = []
    for msg in chat.text_messages:
        messages.append(msg.dict)
    for img in chat.image_messages:
        messages.append(img.dict)

    messages = sorted(messages, key=lambda x: x["timestamp"])
    return jsonify(messages)


def allowed_file(filename):
    return filename.split(".")[-1] in ("png", "jpg", "jpeg")


def save_picture(file):
    random_hex = secrets.token_hex(8)
    filename = random_hex + os.path.splitext(file.filename)[1]
    path = os.path.join(app.root_path, "static", "x-rays", filename)
    file.save(path)
    return filename


@app.post("/chat/<int:id>/image")
def upload_picture(id):
    file = request.files.get("image")
    if file and allowed_file(file.filename):
        filename = save_picture(file)

        timestamp = datetime.utcnow()
        chat = Chat.query.get(id)
        if not chat:
            chat = Chat(user_id=current_user.id)
            db.session.add(chat)
            db.session.commit()

        new_image = ImageMessage(
            chat_id=chat.id, image_path=filename, sender="user", timestamp=timestamp
        )
        db.session.add(new_image)

        bot_response = "Hello, this is a dummy response."
        # Connect to ML prediction pipeline
        bot_msg = TextMessage(
            chat_id=chat.id,
            text=bot_response,
            sender="bot",
            timestamp=timestamp + timedelta(seconds=1),
        )
        db.session.add(bot_msg)
        db.session.commit()

        return jsonify({"bot_response": bot_response, "chat_id": chat.id})

        # old = os.path.join(app.root_path, "static", current_user.image_file)
        # if os.path.exists(old):
        #     os.remove(old)

        # current_user.image_file = filename
        # db.session.commit()
        # return {"message": "File uploaded successfully"}

    return {"message": "Invalid file"}, HTTPStatus.BAD_REQUEST
