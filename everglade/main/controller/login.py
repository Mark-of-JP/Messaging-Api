from flask import Flask, request, make_response
from flask_restful import Resource, Api, reqparse

from everglade.main.service.auth import authLogin, authSighUp
from everglade.main.service.user_service import display_exists, create_user

#Logs in the user
class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        return authLogin(args["email"], args["password"])
    
#Lets the user sign up
class SignUp(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('display_name', type=str)
        args = parser.parse_args()

        if display_exists(args["display_name"]):
            return{"message": 'Display Name Taken' }, 401

        result, status = authSighUp(args["email"], args["password"])

        if status == 200:
            create_user(result['uid'], args["display_name"])
            return {'token': result['token']}
        else:
            return result, status

#Initializes the routes
def initialize_login(api):
    api.add_resource(Login, '/login')
    api.add_resource(SignUp, '/signup')
