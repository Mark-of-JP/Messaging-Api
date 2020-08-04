from flask_socketio import emit, join_room

#You can ignore warnings. Functions are used through their socketio
def initialize_sockets(socketio):
    """Formats the socket so that it is ready for frontend requests
    """
    @socketio.on('message')
    def handle_message(message):
        print('received message: ' + message)

    @socketio.on('connect')
    def test_connect():
        print('connected')
        emit('confirm', {'data': 'Connection Made'})
    
    @socketio.on('marco')
    def marco(pog):
        emit('respond', {'data': pog})

    @socketio.on('join_chats')
    def join_chats(chats):
        emit('pog', {'data': 'Poggers'}, room="pog")
        for chat_id in chats['chats']:
            join_room(chat_id)