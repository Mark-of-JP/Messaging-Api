from flask import Flask, request, make_response
from flask_restful import Resource, Api, reqparse

from everglade.main.constants.error_messages import get_missing_token_error

from everglade.main.service.user_service import get_user_token_info, get_user_info, send_fr, accept_fr, decline_fr, set_user_info, delete_user, remove_friend, get_friend_list, get_users_info, get_user_from_display_name

class TokenUser(Resource):
    def get(self):
        try:
            auth_token = request.headers['EVERGLADE-USER-TOKEN']
        except:
            return get_missing_token_error()

        return get_user_token_info(auth_token)

    def patch(self):
        try:
            auth_token = request.headers['EVERGLADE-USER-TOKEN']
        except:
            return get_missing_token_error()
            
        parser = reqparse.RequestParser()
        parser.add_argument('new_display_name', type=str)
        parser.add_argument('description', type=str)
        args = parser.parse_args()
        new_display_name, description = args['new_display_name'], args['description']

        return set_user_info(auth_token, new_display_name, description)

    def delete(self):
        try:
            auth_token = request.headers['EVERGLADE-USER-TOKEN']
        except:
            return get_missing_token_error()
            
        return delete_user(user_uid)


class MultipleUser(Resource):
    def post(self):
        try:
            auth_token = request.headers['EVERGLADE-USER-TOKEN']
        except:
            return get_missing_token_error()

        parser = reqparse.RequestParser()
        #Users is now a list of strings
        parser.add_argument('users', action='append')
        args = parser.parse_args()

        return get_users_info(args['users'], auth_token)

class User(Resource):
    def get(self, user_uid):
        auth_token = request.headers['EVERGLADE-USER-TOKEN']

        return get_user_info(user_uid, auth_token)

class DisplayUser(Resource):
    def get(self, display_name):
        return get_user_from_display_name(display_name)

class FriendRequest(Resource):
    def patch(self, user_uid):
        parser = reqparse.RequestParser()
        parser.add_argument('receiver', type=str)
        args = parser.parse_args()
        receiver = args['receiver']

        return send_fr(user_uid, receiver)

    def delete(self, user_uid):
        parser = reqparse.RequestParser()
        parser.add_argument('request_id', type=str)
        args = parser.parse_args()
        request_id = args['request_id']

        return decline_fr(user_uid, request_id)

class FriendsList(Resource):
    def get(self, user_uid):
        auth_token = request.headers['EVERGLADE-USER-TOKEN']

        return get_friend_list(user_uid, auth_token)

    def patch(self, user_uid):
        parser = reqparse.RequestParser()
        parser.add_argument('request_id', type=str)
        args = parser.parse_args()
        request_id = args['request_id']

        return accept_fr(user_uid, request_id)

    def delete(self, user_uid):
        parser = reqparse.RequestParser()
        parser.add_argument('friend_id', type=str)
        args = parser.parse_args()
        friend_id = args['friend_id']

        return remove_friend(user_uid, friend_id)
    

    
#Initializes the routes
def initialize_user_routes(api):
    api.add_resource(MultipleUser, '/users')
    api.add_resource(TokenUser, '/users/me')
    api.add_resource(User, '/users/<string:user_uid>')
    api.add_resource(DisplayUser, '/users/<string:display_name>/name')
    api.add_resource(FriendRequest, '/users/<string:user_uid>/friends')
    api.add_resource(FriendsList, '/users/<string:user_uid>/friends/list')