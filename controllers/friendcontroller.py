from flask import flash, redirect,request,url_for,jsonify,session
from dao import FriendDao
from config import server

friend_dao = FriendDao(server.db)

class ControllerFriend:
    def __init__(self) -> None:
        pass

    def seach_user(self):
        username = request.get_json(force = True)
        if username['user'] == '':
            users_find = friend_dao.friend_list(session['user_id'])
        else: 
            users_find = friend_dao.user_search(username['user'],session['user_id'])
        if len(users_find) > 0:
            users_list_json = [user.change_for_json() for user in users_find]
            return jsonify(users_list_json),200
        else:
            return jsonify({'message':'nenhum usuario encontrado'}),204

    @server.loggin_required
    def add_friend(self,id):
        friend_exists = friend_dao.friend_exists(id,session['user_id'])
        if friend_exists or id == session['user_id']:
            flash("voce já é amigo dessa pessoa")
            return redirect(url_for('index'))
        else:
            id = friend_dao.add_friend_in_db(id,session['user_id'])
            return redirect(url_for('index'))