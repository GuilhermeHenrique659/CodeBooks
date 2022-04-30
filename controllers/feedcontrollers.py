from flask import render_template,redirect,session,url_for
from factoryDao import dao
from config import server
from controllers.postcontrollers import ControllerPost



class ControllerFeed:
    def __init__(self) -> None:
        pass

    def index(self):
        if 'login_user' not in session or session['login_user'] == None:
            friend_list = None
            user = None
        else:
            friend_list = dao.friend.friend_list(session['user_id'])
            user = dao.user.search_user_profile(session['user_id'])
        post_list = dao.post.list_post()
        return render_template('base.html', friend_list = friend_list,post_list = post_list, user = user)
