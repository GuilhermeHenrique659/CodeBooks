from flask import flash, redirect,request,url_for,jsonify,session
from factoryDao import dao
from config import server
from models import Notification


class ControllerFriend:
    def __init__(self) -> None:
        pass

    def users_list(self, username):
        if username['user'] == '':
            users_find = dao.friend.friend_list(session['user_id'])
        else: 
            users_find = dao.friend.user_search(username['user'] + "%",session['user_id'])
        return users_find

    @server.loggin_required
    def seach_user(self):
        username = request.get_json(force = True)
        users_find = self.users_list(username)
        if users_find:
            users_list_json = [user.change_for_json() for user in users_find]
            return jsonify(users_list_json),200
        else:
            return jsonify({'message':'nenhum usuario encontrado'}),204

    @server.loggin_required
    def add_friend(self,id,name):
        friend_exists = dao.friend.friend_exists(id,session['user_id'])
        if friend_exists or id == session['user_id']:
            flash("voce já é amigo dessa pessoa")
            return redirect(url_for('user_profile',pag='view', id=id))
        else:
            friendship_id = dao.friend.add_friend_in_db(id,session['user_id'])
            print(name)
            dao.notification.store(Notification(friendship_id,'friend',id, message=f"{session['user_name']} lhe enviou um pedido de amizade"))
            return redirect(url_for('user_profile',pag='view', id=id))

    @server.loggin_required
    def remove_friend(self,id):
        dao.friend.remove_friend(id)
        return redirect(url_for('index'))

    @server.loggin_required
    def confirm_friend(self, id_friendship, id_notification):
        dao.friend.confirm_friend(id_friendship)
        dao.notification.delete(id_notification)
        return jsonify({'message':'friend confirm with success'}),200

    @server.loggin_required
    def reject_friend(self, id_friendship, id_notification):
        dao.friend.remove_friend(id_friendship)
        dao.notification.delete(id_notification)
        return jsonify({'message':'friend reject with success'}),200