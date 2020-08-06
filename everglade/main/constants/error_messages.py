from __future__ import annotations
from typing import Union, Dict, Tuple

def get_missing_token_error() -> Tuple[Dict, int]:
    return { 'message': "EVERGLADE-USER-TOKEN header is missing", "error": "MISSING_TOKEN" }, 401

def get_invalid_token_error() -> Tuple[Dict, int]:
    return { "message": "Token has either expired or is invalid", "error": "INVALID_TOKEN"}, 401

def get_user_not_found_error(message: Union[None, str] = None) -> Tuple[Dict, int]:
    if message is None:
        message = "Error: User does not exist."

    return { "message": message, "error": "USER_DOES_NOT_EXIST" }, 404

def get_chat_not_found_error() -> Tuple[Dict, int]:
    return { "message": "Error: Chat does not exist.", "error": "CHAT_DOES_NOT_EXIST" }, 404

def get_no_access_to_chat_error() -> Tuple[Dict, int]:
    return { "message": "The user has no access to the chat", "error": "USER_HAS_NO_ACCESS_TO_CHAT" }, 401