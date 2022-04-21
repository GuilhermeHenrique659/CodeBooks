from flask import flash, redirect,request,url_for,jsonify,session
from FactoryDao import dao
from config import server


class ControllerFriend:
    def __init__(self) -> None:
        pass

    @server.loggin_required
    def seach_user(self):
        username = request.get_json(force = True)
        if username['user'] == '':
            users_find = dao.friend.friend_list(session['user_id'])
        else: 
            users_find = dao.friend.user_search(username['user'],session['user_id'])
        if len(users_find) > 0:
            users_list_json = [user.change_for_json() for user in users_find]
            return jsonify(users_list_json),200
        else:
            return jsonify({'message':'nenhum usuario encontrado'}),204

    @server.loggin_required
    def add_friend(self,id):
        friend_exists = dao.friend.friend_exists(id,session['user_id'])
        if friend_exists or id == session['user_id']:
            flash("voce já é amigo dessa pessoa")
            return redirect(url_for('user_profile',pag='view', id=id))
        else:
            dao.friend.add_friend_in_db(id,session['user_id'])
            return redirect(url_for('user_profile',pag='view', id=id))

    @server.loggin_required
    def remove_friend(self,id):
        friend_exists = dao.friend.friend_exists(id,session['user_id'])
        if friend_exists:
            flash("Amizade desfeita")
            dao.friend.remove_friend(id,session['user_id'])
            return redirect(url_for('user_profile',pag='view', id=id))
        else:
            flash("usuario nao é seu amigo")
            return redirect(url_for('user_profile',pag='view', id=id))
