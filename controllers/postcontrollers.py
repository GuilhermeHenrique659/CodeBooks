from flask import flash, render_template,request,redirect, session,url_for
from config import server
from factoryDao import dao
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

    @server.loggin_required
    def delete_post(self,id):
        result = dao.post.delete_post(id,session['user_id'])
        if result:
            flash('Erro ao deletar postagem')
            return redirect(url_for('index'))
        flash('Post deletado com sucesso')
        return redirect(url_for('index'))
    
    @server.loggin_required
    def edit_post(self):
        post_data = request.form
        post = Post(post_data['title'],post_data['description'],session['user_id'],idPost=post_data['idpost'])
        dao.post.create_post(post)
        return redirect(url_for('index'))