import os
import secrets
from http import HTTPStatus

from flask import request

from app import app


@app.get("/")
def home():
    return "hidfsd"
