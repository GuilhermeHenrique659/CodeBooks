from flask import flash, render_template,request,redirect, session,url_for
from config import server
from factoryDao import dao
from models import User 
import os



class ControllerUser:
    def __init__(self) -> None:
        pass

    def __render_profile(self, pag, User_profile, id):
        if pag == 'edit' and id == session['user_id']:
            return render_template('profile_edit.html', user = User_profile )
        else:
            post_list:list = dao.post.find_by_user(id)
            if post_list:
                for post in post_list:
                    post.set_files(dao.file.find_all(post._idPost))
            friend_exists = dao.friend.exists(id,session['user_id'])
            return render_template('profile.html', user = User_profile,friend_exists = friend_exists,post_list=post_list)

    @server.loggin_required
    def user_profile(self,id):
        user = dao.user.find_by_id(id)
        if not user:
            return redirect(url_for('index'))
        try:
            pag = request.args['pag']
        except:
            pag = 'view'
        return self.__render_profile(pag, user, id)

    @server.loggin_required
    def user_edit_save(self):
        id = request.args['id']
        user_data_form = request.form
        user_image_file = request.files['image']
        image_filename = self.image_save(id, user_image_file)
        
        user = User(user_data_form['name'],user_data_form['email'],user_data_form['password'],
                    user_data_form['name_complete'],id,user_data_form['age'],
                    image_filename,user_data_form['job'], 
                    user_data_form['city'], user_data_form['state'],
                    user_data_form['bibliografy'])

        try:
            dao.user.store(user)
        except:
            flash("usuario ou email indisponivel")
            return redirect(url_for('user_profile',pag='edit', id=id))
        session['user_name'] = user._name
        session['user_image'] = user.image
        return redirect(url_for('user_profile',pag='view', id=id))

    def image_save(self, id, user_image_file):
        if user_image_file:
            image_filename = f'user_image_profile{id}.jpg'
            upload_folder = server.app.config['UPLOAD_FOLDER']
            user_image_file.save(f'{upload_folder}/{image_filename}')
        else:
            image_filename = session['user_image']
        return image_filename

    @server.loggin_required
    def delete_account(self,id):
        dao.user.delete(id)
        try:
            os.remove(os.path.join(server.app.config['UPLOAD_FOLDER'], f'user_image_profile{id}.jpg'))
        finally:
            return redirect(url_for('logout'))