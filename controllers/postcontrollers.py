from flask import render_template,request,redirect, session,url_for
from config import server
from dao import PostDao, CodeDao
from models import Code, Post

post_dao = PostDao(server.db)
code_dao = CodeDao(server.db)
class ControllerPost:
    def __init__(self) -> None:
        pass

    def list_post(self):
        return post_dao.list_post()
        
    def create_post(self):
        if 'login_user' not in session or session['login_user'] == None:
            return redirect(url_for('login'))
        data_post_front = request.form
        post = Post(data_post_front['title'],data_post_front['description'],session['user_id']) 
        post.set_idPost(post_dao.create_post(post))
        code = Code(data_post_front['code'],post._idPost,session['user_id'])
        result = code_dao.create_code(code)
        return redirect(url_for('index'))