from config import server
from flask_socketio import emit,send, join_room,leave_room, rooms
from flask import render_template, session,request
from factoryDao import dao


class Message:
    def __init__(self, id_user, message) -> None:
        self._id_user = id_user
        self._message = message


chat_history = []

class ControllerChat:

    def find_message_by_room_hash(self, room_hash)->list:
        try:
            return list(filter(lambda item: item['room'] == room_hash, chat_history))
        except:
            pass

    @server.loggin_required
    def chat(self,id):
        id_friendship = dao.friend.exists(id, session['user_id'])
        user_chat = dao.user.find_by_id(id)
        room = id_friendship
        messages_list = self.find_message_by_room_hash(id_friendship)
        return render_template('chat.html',room_hash=room, friend = user_chat,messages_list=messages_list)

    @server.socketio.on('join')
    def on_join(data):
        username = data['user_id']
        room = data['channel']
        join_room(room)
        send(username +' has entered the room.', to=room)

    @server.socketio.on('leave')
    def on_leave(data):
        username = data['user_id']
        room = data['channel']
        leave_room(room)
        send(username + ' has left the room.', to=room)

    @server.socketio.on("send message")
    def message(data):
        room = data['channel']
        chat_history.append({'room':data['channel'],'message':Message(int(data['user_id']),data['message'])})
        emit('getMessage',data, room=room)


    
