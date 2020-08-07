from __future__ import annotations
from typing import List

import uuid
import pyrebase

from everglade.main.constants.constants import config
from everglade.main.model.user_model import UserModel

from everglade.main.constants.error_messages import get_invalid_token_error, get_user_not_found_error

from everglade.main.service.auth import get_info_from_token

def noquote(s):
    return s
pyrebase.pyrebase.quote = noquote

fb = pyrebase.initialize_app(config)
db = fb.database()

def display_exists(display_name: str) -> bool:
    """ Returns true iff a user with that display name exists
    """
    db = fb.database()
    try:
        db.child("users").order_by_child('display_name').equal_to(display_name).get().val()
        return True
    except:
        return False

def user_exists(user_uid: str) -> bool:
    """ Returns true iff a user with that display name exists
    """
    db = fb.database()
    try:
        db.child("users").order_by_child('uid').equal_to(user_uid).get().val()
        return True
    except:
        return False

def on_friends_list(user_uid: str) -> bool:
    database, status = get_user_database(user_uid)
    try:
        if 399 < status < 500:
            raise "Not on friends list"

        database.child('friends_list').child(user_uid).get().val()
        return True
    except:
        return False

def create_user(firebase_uuid: str, display_name: str):
    """ Creates and initializes a user in the user database
    """
    uid = str(uuid.uuid4().int)
    db.child('uids').update({ firebase_uuid: uid })

    user = UserModel(display_name, uid)
    db.child('users').update( {uid: user.get_raw_info()} )

def get_user(user_uid: str):
    return db.child('users').child(user_uid).get().val()

def get_user_from_display_name(display_name: str):
    """ Obtains all the information stored in the user's database from the user's display name and returns it
    """
    db = fb.database()

    try:
        return db.child("users").order_by_child('display_name').equal_to(display_name).get().val(), 200
    except:
        return get_user_not_found_error()

def get_user_database(user_uid: str):
    try:
        if not user_exists(user_uid):
            raise "unpog"
        result = db.child('users').child(user_uid)
    except:
        return get_user_not_found_error()

    return result, 200

def get_user_info(user_uid: str, auth_token: str):
    """ Obtains all the information stored in the user's database and returns it
    """
    #Get info from token and validate token
    try:
        get_user_from_token(auth_token)['user_id']
    except:
        return get_invalid_token_error()
    
    #Get user's database
    database, status = get_user_database(user_uid)

    #Return the error if there is an error with database
    if status < 500 and status > 399:
        return database, status

    #Formats user values and fills missing values
    user_model = UserModel.from_database(database.get().val())

    #Return the information in the user's database
    return user_model.get_raw_info(), 200

def get_users_info(user_uids: List[str], auth_token: str):
    """ Obtains all the information stored in the user's database and returns it for a list of users
    """
    #Get info from token and validate token
    try:
        get_user_from_token(auth_token)['user_id']
    except:
        return get_invalid_token_error()

    users_info = {}

    for user_uid in user_uids:
        #Get user's database
        database, status = get_user_database(user_uid)

        #Return the error if there is an error with database
        if status < 500 and status > 399:
            return database, status

        user_model = UserModel.from_database(database.get().val())
        users_info[user_uid] = user_model.get_raw_info()



    return { "users": users_info }, 200

def get_user_token_info(id_token: str):
    """ Obtains information stored in the user's database for the user with the auth_token
    """

    #Get info from token and validate token
    try:
        firebase_uid = get_user_from_token(id_token)['user_id']
    except:
        return { "message": "Token has either expired or is invalid" }, 401

    #Get uid from token
    db = fb.database()
    token_user = db.child('uids').child(firebase_uid).get().val()

    return get_user_info(token_user, id_token)

def set_user_info(id_token: str, new_display_name: str, description: str):

    if display_exists(new_display_name):
        return {"message": "Error: This username has been taken.", "error": "DISPLAY_NAME_TAKEN"}, 409

    #Get info from token and validate token
    try:
        token_user_firebase_uid = get_user_from_token(id_token)['user_id']
    except:
        return get_invalid_token_error()

    #Get uid from token
    db = fb.database()
    token_user = db.child('uids').child(token_user_firebase_uid).get().val()

    database, status = get_user_database(token_user)

    if status < 500 and status > 399:
        return database, status

    database.update({"description": description})
    database, status = get_user_database(token_user)
    database.update({"display_name": new_display_name})

    database, status = get_user_database(token_user)
    
    #Formats user values and fills missing values
    user_model = UserModel.from_database(database.get().val())
    
    return user_model.get_raw_info(), 200

def delete_user(id_token: str):

    #Get info from token and validate token
    try:
        token_user_firebase_uid = get_user_from_token(id_token)['user_id']
    except:
        return get_invalid_token_error()

    #Get uid from token
    db = fb.database()
    token_user = db.child('uids').child(token_user_firebase_uid).get().val()

    database, status = get_user_database(token_user)

    if 399 < status < 500:
        return database, status
    
    database.remove()
    return {}, 200


def send_fr(id_token: str, receiver: str):

    #Get info from token and validate token
    try:
        token_user_firebase_uid = get_user_from_token(id_token)['user_id']
    except:
        return get_invalid_token_error()

    #Get uid from token
    db = fb.database()
    sender = db.child('uids').child(token_user_firebase_uid).get().val()

    database, status = get_user_database(receiver)
    
    if not user_exists(sender):
        return get_user_not_found_error("Error: Sender user does not exist.")

    if 399 < status < 500:
        return database, status
    
    database.child('friend_requests').update({sender: True})
    
    return {}, 201

def accept_fr(id_token: str, request_id: str):

     #Get info from token and validate token
    try:
        token_user_firebase_uid = get_user_from_token(id_token)['user_id']
    except:
        return get_invalid_token_error()

    #Get uid from token
    db = fb.database()
    user_uid = db.child('uids').child(token_user_firebase_uid).get().val()
    database, status = get_user_database(user_uid)

    if 399 < status < 500:
        return database, status

    if request_id is None:
        return {"message": "Error: Request ID is null. Please use 'request_id'."}, 404

    try:
        if database.child('friend_requests').child(request_id).get().val() is None:
            raise "unpog"
    except:
        return {"message": "Error: Friend request from this user does not exist."}, 404
    
    if on_friends_list(request_id):
        database.child('friend_requests').child(request_id).remove()
        return {"message": "Error: User is already on this friends list."}, 400

    database, status = get_user_database(user_uid)
    database.child('friends_list').update({request_id: True})
    database, status = get_user_database(request_id)
    database.child('friends_list').update({user_uid: True})
    database, status = get_user_database(user_uid)
    database.child('friend_requests').child(request_id).remove()

    #TODO check user isnt already on friends list

    return {}, 200

def decline_fr(id_token: str, request_id: str):
    #Get info from token and validate token
    try:
        token_user_firebase_uid = get_user_from_token(id_token)['user_id']
    except:
        return get_invalid_token_error()

    #Get uid from token
    db = fb.database()
    user_uid = db.child('uids').child(token_user_firebase_uid).get().val()
    database, status = get_user_database(user_uid)

    if 399 < status < 500:
        return database, status

    if request_id is None:
        return {"message": "Error: Request ID is null. Please use 'request_id'."}, 404

    try:
        if database.child('friend_requests').child(request_id).get().val() is None:
            raise "unpog"
    except:
        return {"message": "Error: Friend request from this user does not exist."}, 404
    
    if on_friends_list(request_id):
        database.child('friend_requests').child(request_id).remove()
        return {"message": "Error: User is already on this friends list."}, 400

    database, status = get_user_database(user_uid)
    database.child('friend_requests').child(request_id).remove()

    return {}, 200

def remove_friend(id_token: str, friend_id: str):
    #Get info from token and validate token
    try:
        token_user_firebase_uid = get_user_from_token(id_token)['user_id']
    except:
        return get_invalid_token_error()

    #Get uid from token
    db = fb.database()
    user_uid = db.child('uids').child(token_user_firebase_uid).get().val() 
    database, status = get_user_database(user_uid)

    if 399 < status < 500:
        return database, status
    
    if friend_id is None:
        return {"message": "Error: Friend ID is null. Please use 'friend_id'."}, 404

    try:
        if database.child('friends_list').child(friend_id).get().val() is None:
            raise "unpog"
    except:
        return {"message": "Error: This friend does not exist in this user's friend list."}, 404
    
    database, status = get_user_database(user_uid)
    database.child('friends_list').child(friend_id).remove()
    database, status = get_user_database(friend_id)
    database.child('friends_list').child(user_uid).remove()

    return {}, 200

def get_friend_list(user_uid: str, auth_token: str):
    #Get info from token and validate token
    try:
        get_user_from_token(auth_token)['user_id']
    except:
        return get_invalid_token_error()
        
    database, status = get_user_database(user_uid)

    if 399 < status < 500:
        return database, status

    return database.child("friends_list").get().val(), 200

def get_user_from_token(id_token: str):

    return get_info_from_token(id_token)
