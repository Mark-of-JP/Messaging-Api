from __future__ import annotations
from typing import Dict, List

import time

import pyrebase

from everglade.main.constants.constants import config
from everglade.main.model.chat_model import ChatModel
from everglade.main.model.message_model import MessageModel

from everglade.main.constants.error_messages import get_user_not_found_error, get_invalid_token_error

from everglade.main.service.user_service import user_exists, get_user_database, get_user_from_token
from everglade.main.service.chat_service import chat_exists

from everglade.main.service.socket import emitChatUpdate

fb = pyrebase.initialize_app(config)
db = fb.database()

def message_exists(message_id: str) -> bool:
    """ Returns true iff the message exists
    """

    db = fb.database()

    try:
        if db.child('messages').child(message_id).get().val() is None:
            raise "No message found"

        return True
    except:
        return False

def delete_message(message_id: str, id_token: str) -> Dict:
    """ Deletes a message only if the person deleting the message is the author
    """

    if not message_exists(message_id):
        return get_user_not_found_error()

    db = fb.database()
    message_info = db.child('messages').child(message_id).get().val()
    message = MessageModel.from_ordered_dict(message_info)

    #Get info from token and validate token
    try:
        author_firebase_uid = get_user_from_token(id_token)['user_id']
    except:
        return get_invalid_token_error()

    #Get uid from token
    db = fb.database()
    author = db.child('uids').child(author_firebase_uid).get().val()

    if author != message.author:
        return { 'message': 'Error: User can not delete message.' }, 401

    #Delete message from chat
    if chat_exists(message.chat_id):
        db.child('chats').child(message.chat_id).child('messages').child(message_id).remove()

    #Delete message from messages
    db.child('messages').child(message_id).remove()

    #Inform websockets
    emitChatUpdate(message.chat_id, 'MESSAGE_DELETE', {})

    return { 'message': 'Message deleted' }, 200

def edit_message(message_id: str, edit: str, id_token: str) -> Dict:
    """ Edits the message iff the user wrote the message
    """

    if not message_exists(message_id):
        return {'message': 'Error: Message does not exist.'}, 401

    db = fb.database()
    message_info = db.child('messages').child(message_id).get().val()
    message = MessageModel.from_ordered_dict(message_info)

    #Get info from token and validate token
    try:
        author_firebase_uid = get_user_from_token(id_token)['user_id']
    except:
        return get_invalid_token_error()

    #Get uid from token
    db = fb.database()
    author = db.child('uids').child(author_firebase_uid).get().val()

    if author != message.author:
        return { 'message': 'Error: User can not edit message.' }, 401

    #Editting the message
    message.message = edit
    message.is_editted = True

    result = { message_id: message.get_raw_info() }
    emitChatUpdate(message.chat_id, 'MESSAGE_UPDATE', result)

    return db.child('messages').update(result), 200