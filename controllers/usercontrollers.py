from flask import render_template,request,redirect, session,url_for
from config import server
from factoryDao import dao
from models import User 



class ControllerUser:
    def __init__(self) -> None:
        pass

    def __render_profile(self, pag, User_profile, id):
        if pag == 'edit' and id == session['user_id']:
            return render_template('profile_edit.html', user_profile = User_profile )
        else:
            friend_exists = dao.friend.friend_exists(id,session['user_id'])
            return render_template('profile.html', user_profile = User_profile,friend_exists = friend_exists )

    @server.loggin_required
    def user_profile(self,id):
        User_profile = dao.user.search_user_profile(id)
        if not User_profile:
            return redirect(url_for('index'))
        try:
            pag = request.args['pag']
        except:
            pag = 'view'
        return self.__render_profile(pag, User_profile, id)

    @server.loggin_required
    def user_edit_save(self):
        id = request.args['id']
        user_data_form = request.form
        user_image_file = request.files['image']
        image_filename = f'user_image_profile{id}.jpg'
        user = User(user_data_form['name'],user_data_form['email'],user_data_form['password'],id,
                    user_data_form['age'],image_filename,user_data_form['job'])
        if user_image_file:
            upload_folder = server.app.config['UPLOAD_FOLDER']
            user_image_file.save(f'{upload_folder}/{image_filename}')
        dao.user.save_user(user)
        return redirect(url_for('user_profile',pag='view', id=id))

    @server.loggin_required
    def delete_account(self,id):
        dao.user.delete_user(id)
        return redirect(url_for('logout'))