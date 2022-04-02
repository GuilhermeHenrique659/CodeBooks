from flask import render_template,redirect,session,url_for
from dao import FriendDao
from config import server

friend_dao = FriendDao(server.db)
class ControllerFeed:
    def __init__(self) -> None:
        pass

    def index(self):
        if 'login_user' not in session or session['login_user'] == None:
            friend_list = None
        else:
            friend_list = friend_dao.friend_list(session['user_id'])
        return render_template('base.html', friend_list = friend_list)