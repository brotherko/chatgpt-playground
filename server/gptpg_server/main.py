import time
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from asgiref.wsgi import WsgiToAsgi

from os import environ

from .classes.session import ChatSession
from .classes.handler import ChatHandler
from .classes.session_manager import ChatSessionManager

logging.basicConfig(level=logging.DEBUG)

session_manager = ChatSessionManager()
ChatSession.set_chat_handler(ChatHandler.getInstance())

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DB_CONNECTION_STRING")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cors = CORS(app)
asgi_app = WsgiToAsgi(app)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("session.id"))
    sender = db.Column(db.String(10))
    message = db.Column(db.String(5000))
    created_at = db.Column(db.DateTime)

with app.app_context():
    db.create_all()

@app.get("/health")
def health():
    isHealthy = ChatHandler.getInstance().healthcheck()
    if (not isHealthy):
        return "unhealthy", 500
    return "healthy", 200

@app.get("/chat/<session_id>")
def get_chat(session_id):
    session = session_manager.get(session_id)
    return jsonify(session.get_conversations())

@app.post("/chat/<session_id>")
def post_chat(session_id):
    message = request.get_json().get('message')
    session = session_manager.get(session_id)

    answer = session.handle_ask(message)

    return jsonify({"answer": answer})

def start_dev():
    app.run()