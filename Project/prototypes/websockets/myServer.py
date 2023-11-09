import socketio
import eventlet

# Create a Socket.IO server instance
sio = socketio.Server()

# Define an event handler for when a client connects
@sio.on('connect')
def connect(sid, environ):
    print(f"Client {sid} connected")

@sio.on('join_room')
def join_room(sid, room):
    sio.enter_room(sid, room)
    print(f"Client {sid} joined room {room}")

@sio.on('leave_room')
def leave_room(sid, room):
    sio.leave_room(sid, room)
    print(f"Client {sid} left room {room}")

@sio.on('get_lobbies')
def get_lobbies(sid, data):
    pass

# Define an event handler for when a client sends a message
@sio.on('message')
def message(sid, data):
    print(f"Received message from client {sid}: {data}")

    #Send the message to all clients in the specified room
    room = data.get('room')
    sio.emit('message', data['message'], room=room)

# Define an event handler for when a client disconnects
@sio.on('disconnect')
def disconnect(sid):
    print(f"Client {sid} disconnected")

if __name__ == '__main__':
    # Wrap the Socket.IO server with a WSGI application
    app = socketio.WSGIApp(sio)

    # Create an eventlet server to serve the WSGI application
    eventlet.wsgi.server(eventlet.listen(('localhost', 3000)), app)
