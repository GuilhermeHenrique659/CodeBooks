from flask import render_template,redirect,session,url_for
from dao import FriendDao, UserDao
from config import server
from controllers.postcontrollers import ControllerPost

friend_dao = FriendDao(server.db)
user_dao = UserDao(server.db)
post_controller = ControllerPost()


class ControllerFeed:
    def __init__(self) -> None:
        pass

    def index(self):
        if 'login_user' not in session or session['login_user'] == None:
            friend_list = None
            user = None
        else:
            friend_list = friend_dao.friend_list(session['user_id'])
            user = user_dao.search_user_profile(session['user_id'])
        post_list = post_controller.list_post()
        
        return render_template('base.html', friend_list = friend_list,post_list = post_list, user = user)
