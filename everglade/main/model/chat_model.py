from __future__ import annotations
from typing import Dict, OrderedDict

class ChatModel:

    def __init__(self, uuid, name, members, messages):
        self.uuid = uuid
        self.name = name
        self.members = members
        self.messages = messages

    @classmethod
    def from_ordered_dict(cls, chat_id: str, query_info: OrderedDict) -> ChatModel:
        formatted_members = list(query_info['members'].keys())
        formatted_messages = query_info.get('messages', None)

        return ChatModel(chat_id, query_info['chat_name'], formatted_members, formatted_messages)


    def get_raw_info(self) -> Dict:
        """Gets the info from the chat model in dictionary form
        """

        formatted_members = {}
        for member in self.members:
            formatted_members[member] = True

        return {
            self.uuid: {
                "chat_name": self.name,
                "members": formatted_members,
                "messages": self.messages 
            }
        }