from config import server
from flask_socketio import emit,send, join_room,leave_room
from flask import render_template, session,request
from factoryDao import dao


id_friend = None

class ControllerChat:

    @server.loggin_required
    def chat(self,id):
        user_chat = dao.user.search_user_profile(id)
        return render_template('chat.html',id_friend=id, friend = user_chat)

    @server.socketio.on('join')
    def on_join(data):
        username = data['username']
        room = data['channel']
        join_room(room)
        send(' has entered the room.', to=room)

    @server.socketio.on('leave')
    def on_leave(data):
        username = data['username']
        room = data['room']
        leave_room(room)
        send(' has left the room.', to=room)

    @server.socketio.on("send message")
    def message(data):
        room = data['channel']
        emit('getMessage',data, room=room)