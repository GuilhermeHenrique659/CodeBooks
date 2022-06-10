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
        else:
            friend_list:list = dao.friend.findAll_by_user(session['user_id'])
        post_list:list = dao.post.findall()
        self.set_files_of_post_list(post_list)
        return render_template('index.html', friend_list = friend_list,post_list = post_list)

    def set_files_of_post_list(self, post_list):
        if post_list:
            for post in post_list:
                post:Post
                post.set_files(dao.file.find_all(post._idPost))
