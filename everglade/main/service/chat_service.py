from __future__ import annotations
from typing import Dict, List

import time

import uuid
import pyrebase
from flask_socketio import emit

from everglade.main.constants.constants import config, get_default_chat_uid
from everglade.main.model.chat_model import ChatModel
from everglade.main.model.message_model import MessageModel

from everglade.main.constants.error_messages import get_invalid_token_error, get_user_not_found_error, get_chat_not_found_error, get_no_access_to_chat_error

from everglade.main.service.socket import emitUserUpdate, emitChatUpdate
from everglade.main.service.user_service import user_exists, get_user_database, get_user_from_token

fb = pyrebase.initialize_app(config)
db = fb.database()

def chat_exists(chat_uid: str) -> bool:
    """ Returns true iff the chat exists
    """

    db = fb.database()

    try:
        if db.child('chats').child(chat_uid).child('chat_name').get().val() is None:
            raise "No chat found"

        return True
    except:
        return False

def user_has_access(chat_id: str, user_id: str) -> bool:
    """ Returns true iff the user has access to the chat
    """

    db = fb.database()

    try:
        if db.child('chats').child(chat_id).child('members').child(user_id).get().val() is None:
            raise "The user has no access to the chat"

        return True
    except:
        return False

def create_chat(name: str, id_token: str) -> Dict:
    """ Creates a chat using a chat name and the initial_member who made it. 
    Requires an idToken for verification
    """

    #Get info from token and validate token
    try:
        token_user_firebase_uid = get_user_from_token(id_token)['user_id']
    except:
        return get_invalid_token_error()

    #Get uid from token
    db = fb.database()
    initial_member = db.child('uids').child(token_user_firebase_uid).get().val()

    database, status = get_user_database(initial_member)
    if 400 <= status < 500:
        return database, status 

    chat_uuid = uuid.uuid4()
    chat_uuid = str(chat_uuid.int)

    chat = ChatModel(chat_uuid, name, [initial_member], {})

    database.child('chats').update({ chat_uuid: True })
    db.child("chats").update(chat.get_raw_info())

    return db.child("chats").update(chat.get_raw_info()), 201

def get_chat(chat_uuid: str, id_token: str, message_limit: int) -> Dict:
    """ Gets and formats a chat from the database
    """

    if not chat_exists(chat_uuid):
        return get_chat_not_found_error()

    #Get info from token and validate token
    try:
        token_user_firebase_uid = get_user_from_token(id_token)['user_id']
    except:
        return get_invalid_token_error()

    #Get uid from token
    db = fb.database()
    token_user = db.child('uids').child(token_user_firebase_uid).get().val()

    #Check if user is in the chat
    if not user_has_access(chat_uuid, token_user):
        return get_no_access_to_chat_error()

    #Grabbing messages with limit
    messages = []
    messages_ordered_dict = db.child('chats').child(chat_uuid).child('messages').order_by_child('time').limit_to_last(message_limit).get().val()
    if messages_ordered_dict is not None and len(messages_ordered_dict) > 0:
        for message_id in list(messages_ordered_dict.keys()):
            raw_message = db.child('messages').child(message_id).get().val()
            message = MessageModel.from_ordered_dict(query_info=raw_message)

            formatted_massage = message.get_raw_info()
            
            author_display_name = db.child('users').child(message.author).child("display_name").get().val()
            formatted_massage["author_display_name"] = author_display_name

            messages.append(formatted_massage)

    #Format chat info
    db = fb.database()
    chat_info = db.child('chats').child(chat_uuid).get().val()
    chat_info['messages'] = messages
    return chat_info, 200

def get_simple_chat(chat_uuid: str, id_token: str) -> Dict:
    """ Gets the simplified information for chats
    """

    if not chat_exists(chat_uuid):
        return get_chat_not_found_error()

    #Get info from token and validate token
    try:
        get_user_from_token(id_token)['user_id']
    except:
        return get_invalid_token_error()

    simple_info = {}

    #Format chat info
    db = fb.database()
    chat_name = db.child('chats').child(chat_uuid).child('chat_name').get().val()

    simple_info['chat_name'] = chat_name

    return simple_info

def send_message(chat_uuid: str, message: str, id_token: str) -> Dict:
    """ Creates a message for the chat with the corresponding chat_uuid.
    The time should be in the millisecond time format.
    Requires an idToken for verification.
    """

    if not chat_exists(chat_uuid):
        return get_chat_not_found_error()

    #Get info from token and validate token
    try:
        token_user_firebase_uid = get_user_from_token(id_token)['user_id']
    except:
        return get_invalid_token_error()

    #Get uid from token
    db = fb.database()
    token_user = db.child('uids').child(token_user_firebase_uid).get().val()

    if not user_exists(token_user):
        return get_user_not_found_error()

    message_uuid = str(uuid.uuid4().int)

    message_model = MessageModel(message_uuid, message, token_user, int(round(time.time() * 1000)), chat_uuid)

    #Add message uuid to chat
    db = fb.database()
    db.child('chats').child(chat_uuid).child('messages').update({ message_uuid: {"time": message_model.time} })

    #Message
    db = fb.database()
    result = db.child('messages').update({ message_uuid: message_model.get_raw_info() })

    #Notifying Websockets
    emitChatUpdate(chat_uuid, "MESSAGE_SENT", result)

    return result, 201

def delete_chat(chat_id: str, id_token: str) -> Dict:
    """ Deletes the chat if user is a member of the chat
    """

    if chat_id == get_default_chat_uid():
        return { "message": "You can not delete the default chat", "error": "CANT_DELETE_CHAT" }, 401

    if not chat_exists(chat_id):
        return get_chat_not_found_error()

    #Get info from token and validate token
    try:
        token_user_firebase_uid = get_user_from_token(id_token)['user_id']
    except:
        return get_invalid_token_error()

    #Get uid from token
    db = fb.database()
    token_user = db.child('uids').child(token_user_firebase_uid).get().val()

    #Check if user is in the chat
    db = fb.database()
    if not user_has_access(chat_id, token_user):
        return get_no_access_to_chat_error()

    #Get chat
    chat_info = db.child('chats').child(chat_id).get().val()
    chat = ChatModel.from_ordered_dict(chat_id, chat_info)
    
    #Delete chat
    db = fb.database()
    db.child('chats').child(chat_id).remove()    

    #Delete members
    for member in chat.members:
        db.child('users').child(member).child('chats').child(chat_id).remove()

    #Delete messages
    if chat.messages is not None:
        for message in chat.messages.keys():
            db.child('messages').child(message).remove()

    #Notifying websockets
    emitChatUpdate(chat_id, 'CHAT_DELETED', {})

    return { 'message': 'Chat deleted' }, 200

def send_chat_request(chat_id: str, receiver: str, id_token: str) -> Dict:
    """ Sends the receiver a chat request iff the sender (id_token) is a part of the chat
    """

    if not chat_exists(chat_id):
        return get_chat_not_found_error()

    #Get info from token and validate token
    try:
        token_user_firebase_uid = get_user_from_token(id_token)['user_id']
    except:
        return get_invalid_token_error()

    #Check if receiver exists
    if not user_exists(receiver):
        return get_user_not_found_error()

    #Get uid from token
    db = fb.database()
    token_user = db.child('uids').child(token_user_firebase_uid).get().val()

    #Check if user is in the chat
    db = fb.database()
    if not user_has_access(chat_id, token_user):
        return get_no_access_to_chat_error()

    #Add chat request to user
    db.child('users').child(receiver).child('chat_requests').update({ chat_id: True })

    #Notifying Websockets
    emitUserUpdate(receiver, "Chat_request_sent", chat_id)

    return { 'message': 'Invite sent' }, 201

def accept_chat_request(chat_id: str, id_token: str) -> Dict:
    """ Accepts a chat request
    """

    if not chat_exists(chat_id):
        return get_chat_not_found_error()

    #Get info from token and validate token
    try:
        token_user_firebase_uid = get_user_from_token(id_token)['user_id']
    except:
        return get_invalid_token_error()

    #Get uid from token
    db = fb.database()
    token_user = db.child('uids').child(token_user_firebase_uid).get().val()

    #Check if user has been invited to the chat
    if db.child('users').child(token_user).child('chat_requests').child(chat_id).get().val() is None:
        return { 'message': 'Error: User has not been invited to chat' }, 401

    #Add user to chat
    db.child('chats').child(chat_id).child('members').update({ token_user: True })
    db.child('users').child(token_user).child('chat_requests').child(chat_id).remove()
    db.child('users').child(token_user).child('chats').update({ chat_id: True })

    return { 'message': 'User has been invited to the chat' }, 200

def decline_chat_request(chat_id: str, id_token: str) -> Dict:
    """ Decline a chat request
    """

    if not chat_exists(chat_id):
        return get_chat_not_found_error()

    #Get info from token and validate token
    try:
        token_user_firebase_uid = get_user_from_token(id_token)['user_id']
    except:
        return get_invalid_token_error()

    #Get uid from token
    db = fb.database()
    token_user = db.child('uids').child(token_user_firebase_uid).get().val()

    #Check if user has been invited to the chat
    if db.child('users').child(token_user).child('chat_requests').child(chat_id).get().val() is None:
        return { 'message': 'Error: User has not been invited to chat' }, 401

    #Add user to chat
    db.child('users').child(token_user).child('chat_requests').child(chat_id).remove()

    return { 'message': 'User has declined' }, 200

def leave_chat(chat_id: str, id_token: str) -> Dict:
    """ Leave a chat
    """

    if not chat_exists(chat_id):
        return get_chat_not_found_error()

    #Get info from token and validate token
    try:
        token_user_firebase_uid = get_user_from_token(id_token)['user_id']
    except:
        return get_invalid_token_error()

    #Check if receiver exists
    if not user_exists(receiver):
        return get_user_not_found_error()

    #Get uid from token
    db = fb.database()
    token_user = db.child('uids').child(token_user_firebase_uid).get().val()

    #Check if user is in the chat
    db = fb.database()
    if not user_has_access(chat_id, token_user):
        return get_no_access_to_chat_error()

    db = fb.database()
    db.child('users').child(token_user).child('chats').child(chat_id).remove()
    db = fb.database()
    db.child('chats').child(chat_id).child('members').child(token_user).remove()