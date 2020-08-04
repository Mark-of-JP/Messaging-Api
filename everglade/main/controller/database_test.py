import pyrebase

from flask import Flask, request, make_response
from flask_restful import Resource, Api, reqparse

from everglade.main.service.ignore.config import config
from everglade.main.service.user_service import get_user_database

def noquote(s):
    return s
pyrebase.pyrebase.quote = noquote

fb = pyrebase.initialize_app(config)
db = fb.database()

class DataTest(Resource):
    def get(self):
        get_user_database("SoftBoiUwu")
        return { 'eat': 'nut'}


class DataPog(Resource):
    def get(self):
        
        print(db.child("search").order_by_child('test').equal_to('dracon').get().val())
        return { 'nut': 'nut'}

def initialize_database_test(api):
    api.add_resource(DataTest, '/dataTest')
    api.add_resource(DataPog, '/dataPog')