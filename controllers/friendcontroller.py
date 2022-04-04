from flask import flash, redirect,request,url_for,jsonify,session
from dao import FriendDao
from config import server

friend_dao = FriendDao(server.db)

class ControllerFriend:
    def __init__(self) -> None:
        pass

    def seach_user(self):
        if 'login_user' not in session or session['login_user'] == None:
            return redirect(url_for('login'))
        username = request.get_json(force = True)
        users_find = friend_dao.user_search(username['user'],session['user_id'])
        users_list_json = [user.change_for_json() for user in users_find]
        return jsonify(users_list_json)

    def add_friend(self,id):
        if 'login_user' not in session or session['login_user'] == None:
            return redirect(url_for('login'))
        friend_exists = friend_dao.friend_exists(id,session['user_id'])
        if friend_exists or id == session['user_id']:
            flash("voce já é amigo dessa pessoa")
            return redirect(url_for('index'))
        else:
            id = friend_dao.add_friend_in_db(id,session['user_id'])
            return redirect(url_for('index'))