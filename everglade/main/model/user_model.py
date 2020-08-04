from __future__ import annotations
from typing import Dict

class UserModel:
    
    def __init__(self, display_name, uid, friends = {}, chats = {}, friend_requests = {}, chat_requests = {}):
        self.uid = uid
        self.display_name = display_name

        self.friends = friends
        self.chats = chats

        self.friend_requests = friend_requests
        self.chat_requests = chat_requests

    @classmethod
    def from_database(cls, data: Dict):
        user = UserModel(data['display_name'], data['uid'], data.get('friends_list', {}), data.get('chats', {}), data.get('friend_requests', {}), data.get('chat_requests', {}))

        return user

    def get_raw_info(self):
        info = {
            "display_name": self.display_name,
            "uid": self.uid,
            
            "chats": self.chats,
            "friends_list": self.friends,

            "chat_requests": self.chat_requests,
            "friend_requests": self.friend_requests
        }

        return info