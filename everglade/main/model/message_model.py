from __future__ import annotations
from typing import Dict, OrderedDict

class MessageModel:

    def __init__(self, message_id, message, author, time, chat_id, is_editted = False):
        self.message_id = message_id
        self.message = message
        self.author = author
        self.time = time
        self.chat_id = chat_id
        self.is_editted = is_editted

    @classmethod
    def from_ordered_dict(cls, query_info: OrderedDict) -> MessageModel:
        return MessageModel(query_info['uid'], query_info['message'], query_info['author'], query_info['time'], query_info['chat'], query_info.get('is_editted', False))

    def get_raw_info(self) -> Dict:
        """Gets the info from the message model in dictionary form
        """
        return {
            "message": self.message,
            "author": self.author,
            "time": str(self.time),
            "chat": self.chat_id,
            "uid": self.message_id,
            "is_editted": self.is_editted
        }
