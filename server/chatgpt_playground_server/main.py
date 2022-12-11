import time
import logging

from os import environ

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from .classes.handler import ChatHandler
from .classes.session import ChatSession
from .classes.session_manager import ChatSessionManager

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

session_manager = ChatSessionManager()

chat_handler = ChatHandler(
    email=environ.get('OPENAI_EMAIL'),
    password=environ.get("OPENAI_PASSWORD"),
    proxies=environ.get("OPENAI_PROXY"))

ChatSession.set_chat_handler(chat_handler)

@app.get("/api/chat/<session_id>")
def get_chat(session_id):
    session = session_manager.get(session_id)
    return jsonify(session.get_conversations())

@app.post("/api/chat/<session_id>")
def post_chat(session_id):
    message = request.get_json().get('message')
    session = session_manager.get(session_id)

    answer = session.handle_ask(message)

    return jsonify({"answer": answer})

def start_dev():
    app.run()