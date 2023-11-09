import socketio
import sys

sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('Connected to the server')

@sio.on('message')
def on_message(data):
    print('Received message:', data)

sio.connect('http://127.0.0.1:3000')

room_name = sys.argv[1]

sio.emit('join_room', room_name)

while True:
    message = input("Enter a message (or 'exit' to quit): ")
    if message == 'exit':
        break
    message = {'room':room_name, 'message':message}

    sio.emit('message', message)

sio.emit('leave_room', room_name)


sio.disconnect()
