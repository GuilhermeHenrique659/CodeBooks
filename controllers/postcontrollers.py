
from flask import flash, render_template,request,redirect, session,url_for
from config import server
from factoryDao import dao
from models import Code, File, Post
import os
from validation.fileValidation import validation_file

class ControllerPost:

    @server.loggin_required
    def create_post(self):
        post_form = request.form
        post_files = request.files.getlist('files[]')
        post = Post(post_form['title'],post_form['description'],session['user_id']) 
        post.set_idPost(dao.post.store(post))
        code = Code(post_form['code'],post._idPost,session['user_id'])
        dao.code.store(code)
        self.file_validation(post_files, post)
        return redirect(url_for('index'))

    def file_validation(self, post_files, post):
        if post_files[0].filename != '':
            for i in range(len(post_files)):
                if validation_file.isImageValid(validation_file.type_file(post_files[i].filename)): 
                    self.save_image(post_files,post,i)
                elif validation_file.isVideoValid(validation_file.type_file(post_files[i].filename)):
                    self.save_movie(post_files,post,i)
                else:
                    flash('Arquivo não aceita')

    def save_movie(self, post_files, post:Post, i):
        file_name = f'post_video{post._idPost}{i}.mp4'
        upload_folder = server.app.config['UPLOAD_FOLDER']
        post_files[i].save(f'{upload_folder}/{file_name}')
        file = File(file_name,'video',post._idPost)
        dao.file.store(file)

    def save_image(self, post_files, post:Post, i):
        file_name = f'post_image{post._idPost}{i}.jpg'
        upload_folder = server.app.config['UPLOAD_FOLDER']
        post_files[i].save(f'{upload_folder}/{file_name}')
        file = File(file_name,'image',post._idPost)
        dao.file.store(file)

    def delete_files(self, filelist: list):
        if filelist:
            for file in filelist:
                os.remove(os.path.join(server.app.config['UPLOAD_FOLDER'], f'{file._filename}'))
        
    @server.loggin_required
    def delete_post(self,id):
        self.delete_files(dao.file.find_all(id))
        dao.post.delete(id,session['user_id'])    
        flash('Post deletado com sucesso')
        return redirect(url_for('index'))
    
    @server.loggin_required
    def edit_post(self):
        post_data = request.form
        post = Post(post_data['title'],post_data['description'],session['user_id'],idPost=post_data['idpost'])
        dao.post.store(post)
        return redirect(url_for('index'))