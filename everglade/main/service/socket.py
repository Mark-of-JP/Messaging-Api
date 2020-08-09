from __future__ import annotations
from typing import Any

from flask_socketio import emit, join_room

#You can ignore warnings. Functions are used through their socketio
def initialize_sockets(socketio):
    """Formats the socket so that it is ready for frontend requests
    """
    @socketio.on('message')
    def handle_message(message):
        print('received message: ' + message)

    @socketio.on('connect')
    def test_connect():
        print('connected')
        emit('confirm', {'data': 'Connection Made'})
    
    @socketio.on('marco')
    def marco(pog):
        emit('respond', {'data': pog})

    @socketio.on('join_chats')
    def join_chats(chats):
        for chat_id in chats['chats']:
            join_room(chat_id)

    @socketio.on('connect_user')
    def join_chats(user):
        join_room(user['uid'])

def emitChatUpdate(chat_id: str, message: str, payload: Any) -> None:
    """ Emits the chat_updated event to members of chat
    """
    emit('chat_updated', { "chat": chat_id, "message": message, "payload": payload }, room=chat_id, namespace="/")

def emitUserUpdate(user_id: str, message: str, payload: Any) -> None:
    """ Emits the user_updated event to the user
    """
    emit('user_updated', { "user": user_id, "message": message, "payload": payload }, room=user_id, namespace="/")