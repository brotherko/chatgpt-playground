import string
import logging
import time
from enum import Enum

class Sender(str, Enum):
    HUMAN = "human",
    AI = "ai"


class ChatSession:
    __chat_handler = None

    def __init__(self, id):
        self.id = id

        self.__conversations: list = []
        self.__conversation_id: str = None
        self.__previous_convo_id: str = None


    @staticmethod
    def set_chat_handler(chat_handler):
        ChatSession.__chat_handler = chat_handler

    def handle_ask(self, message):
        self._add_conversation(Sender.HUMAN, message)

        response = ChatSession.__chat_handler.ask(message, self.__conversation_id, self.__previous_convo_id)
        # time.sleep(3)
        # response = ("fake reply", 1, 1)

        answer, previous_convo_id, conversation_id = response
        logging.info(f"Chat GPT Response = {answer}")

        self._set_conversation_id_if_not(conversation_id)
        self.__previous_convo_id = previous_convo_id
        self._add_conversation(Sender.AI, answer)

        return answer

    def _add_conversation(self, sender, message):
        logging.info(f"adding conversation: session_id = {self.id}, sender = {sender}, message = {message}")
        convo = {
            "sender": sender,
            "message": message
        }
        self.__conversations.append(convo)
    
    def _set_conversation_id_if_not(self, conversation_id):
        if (not self.__conversation_id):
            self.__conversation_id = conversation_id

    def get_conversations(self):
        return self.__conversations