from .session import ChatSession

class ChatSessionManager:
  __sessions = {}

  @staticmethod
  def get(session_id):
    if (session_id not in ChatSessionManager.__sessions):
      ChatSessionManager.__sessions[session_id] = ChatSession(session_id)

    return ChatSessionManager.__sessions[session_id]