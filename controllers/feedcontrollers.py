from flask import render_template,redirect,session,url_for
from factoryDao import dao
from config import server
from models import Post



class ControllerFeed:
    def __init__(self) -> None:
        pass

    def index(self):
        if 'login_user' not in session or session['login_user'] == None:
            friend_list = None
            user = None
        else:
            friend_list:list = dao.friend.friend_list(session['user_id'])
            user = dao.user.search_user_profile(session['user_id'])
        post_list:list = dao.post.list_post()
        if post_list:
            for post in post_list:
                post:Post
                post.set_files(dao.file.findall_files(post._idPost))
        return render_template('index.html', friend_list = friend_list,post_list = post_list, user = user)
