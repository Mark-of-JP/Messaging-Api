from flask import Flask, request, make_response
from flask_restful import Resource, Api, reqparse

from everglade.main.service.chat_service import create_chat, send_message, get_chat, get_simple_chat, delete_chat, send_chat_request, accept_chat_request, decline_chat_request
from everglade.main.service.message_service import delete_message, edit_message

class CreateChat(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('chat_name', type=str)
        args = parser.parse_args()

        id_token = request.headers['EVERGLADE-USER-TOKEN']

        return create_chat(args['chat_name'], id_token)

class Chat(Resource):
    def get(self, chat_id):
        id_token = request.headers['EVERGLADE-USER-TOKEN']
        message_limit = int(request.args.get('message_limit'))

        return get_chat(chat_id, id_token, message_limit)

    def post(self, chat_id):
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str)
        args = parser.parse_args()

        id_token = request.headers['EVERGLADE-USER-TOKEN']

        return send_message(chat_id, args['message'], id_token)

    def delete(self, chat_id):
        id_token = request.headers['EVERGLADE-USER-TOKEN']

        return delete_chat(chat_id, id_token)

class SimpleChat(Resource):
    def get(self, chat_id):
        id_token = request.headers['EVERGLADE-USER-TOKEN']

        return get_simple_chat(chat_id, id_token)

class Message(Resource):
    def delete(self, message_id):
        id_token = request.headers['EVERGLADE-USER-TOKEN']

        return delete_message(message_id, id_token)
    
    def patch(self, message_id):
        parser = reqparse.RequestParser()
        parser.add_argument('edit', type=str)
        args = parser.parse_args()

        id_token = request.headers['EVERGLADE-USER-TOKEN']

        return edit_message(message_id, args['edit'], id_token)

class Invite(Resource):
    def put(self, chat_id):
        parser = reqparse.RequestParser()
        parser.add_argument('receiver', type=str)
        args = parser.parse_args()

        id_token = request.headers['EVERGLADE-USER-TOKEN']

        return send_chat_request(chat_id, args['receiver'], id_token)

class Accept(Resource):
    def put(self, chat_id):
        id_token = request.headers['EVERGLADE-USER-TOKEN']

        return accept_chat_request(chat_id, id_token)

class Decline(Resource):
    def put(self, chat_id):
        id_token = request.headers['EVERGLADE-USER-TOKEN']

        return decline_chat_request(chat_id, id_token)


#Initializes the routes
def initialize_chat_routes(api):
    api.add_resource(CreateChat, '/create/chat')
    api.add_resource(Chat, '/chat/<string:chat_id>')
    api.add_resource(SimpleChat, '/chat/<string:chat_id>/simple')
    api.add_resource(Invite, '/chat/<string:chat_id>/invite')
    api.add_resource(Accept, '/chat/<string:chat_id>/accept')
    api.add_resource(Decline, '/chat/<string:chat_id>/decline')
    api.add_resource(Message, '/message/<string:message_id>')