from flask import render_template,request,redirect, session,url_for
from config import server
from FactoryDao import dao
from models import Code, Post


class ControllerPost:
    def __init__(self) -> None:
        pass

    def list_post(self):
        return dao.post.list_post()
        
    @server.loggin_required
    def create_post(self):
        data_post_front = request.form
        post = Post(data_post_front['title'],data_post_front['description'],session['user_id']) 
        post.set_idPost(dao.post.create_post(post) )
        code = Code(data_post_front['code'],post._idPost,session['user_id'])
        result = dao.code.create_code(code)
        return redirect(url_for('index'))

