from config import server
from flask_socketio import emit,send, join_room,leave_room
from flask import render_template, session,request
from factoryDao import dao

class ControllerChat:

    @server.loggin_required
    def chat(self,id):
        user_chat = dao.user.find_by_id(id)
        friend_hash = hash(user_chat._email)
        user_hash = hash(session['login_user'])
        room_hash = user_hash + friend_hash
        return render_template('chat.html',room_hash=room_hash, friend = user_chat)

    @server.socketio.on('join')
    def on_join(data):
        username = data['username']
        room = data['channel']
        join_room(room)
        send(username +' has entered the room.', to=room)

    @server.socketio.on('leave')
    def on_leave(data):
        username = data['username']
        room = data['channel']
        leave_room(room)
        send(username + ' has left the room.', to=room)

    @server.socketio.on("send message")
    def message(data):
        room = data['channel']
        emit('getMessage',data, room=room)
