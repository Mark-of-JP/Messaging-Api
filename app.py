import os

from everglade.main.controller.init_controller import initialize_all_controllers
from everglade.main.service.socket import initialize_sockets

from flask import Flask, request, make_response
from flask_restful import Resource, Api
from flask_socketio import SocketIO, emit
from flask_cors import CORS

import everglade.main.service.socket

#Initializes the app through flask, socketio and restful
app = Flask(__name__)
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*", always_connect=True)
api = Api(app)

#Sets the CORS policy to allow origin to connect
CORS(app, allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials", "EVERGLADE-USER-TOKEN", "Cache-Control",
    "Sec-WebSocket-Accept", "Sec-WebSocket-Extensions", "Sec-WebSocket-Key", "Sec-WebSocket-Protocol", "Sec-WebSocket-Version"],
    supports_credentials=True)

class HelloWorld(Resource):
    def get(self):
        return {"about": "It works!"}

api.add_resource(HelloWorld, '/')

#Initializes controllers and sockets
initialize_all_controllers(api)
initialize_sockets(socketio)

if __name__ == "__main__":
    if os.environ.get('IS_HEROKU', False):
        socketio.run(app, host = "0.0.0.0", port = int(os.environ.get('PORT', 8080)), debug=True) #Run this on the production server
    else:
        socketio.run(app, debug=True) #Run this for local server