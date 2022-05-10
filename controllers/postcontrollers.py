from flask import flash, render_template,request,redirect, session,url_for
from config import server
from factoryDao import dao
from models import Code, File, Post
import os

class ControllerPost:
    def __init__(self) -> None:
        pass
        
    @server.loggin_required
    def create_post(self):
        post_form = request.form
        post_files = request.files.getlist('files')
        post = Post(post_form['title'],post_form['description'],session['user_id']) 
        post.set_idPost(dao.post.create_post(post) )
        code = Code(post_form['code'],post._idPost,session['user_id'])
        dao.code.create_code(code)
        if post_files:
            for i in range(len(post_files)):
                file_name = f'post_image{post._idPost}{i}.jpeg'
                upload_folder = server.app.config['UPLOAD_FOLDER']
                post_files[i].save(f'{upload_folder}/{file_name}')
                file = File(file_name,'image',post._idPost)
                dao.file.save_files(file)
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