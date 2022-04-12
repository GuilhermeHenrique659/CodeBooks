from flask import render_template,request,redirect, session,url_for
from config import server
from dao import UserDao
from models import User 


user_dao = UserDao(server.db)


class ControllerUser:
    def __init__(self) -> None:
        pass
    def user_profile(self):
        if 'login_user' not in session or session['login_user'] == None:
            return redirect(url_for('login'))
        User_profile = user_dao.search_user_profile(session['user_id'])
        try:
            pag = request.args['pag']  
        except:
            pag = None      
        if(pag == 'edit'):
            return render_template('profile_edit.html', user_profile = User_profile )
        else:
            return render_template('profile.html', user_profile = User_profile )

    def user_edit_save(self):
        if 'login_user' not in session or session['login_user'] == None:
            return redirect(url_for('login'))
        id = request.args['id']
        user_data_form = request.form
        user_image_file = request.files['image']
        image_filename = f'user_image_profile{id}.jpg'
        user = User(user_data_form['name'],user_data_form['email'],user_data_form['password'],id,
                    user_data_form['age'],image_filename,user_data_form['job'])
        if user_image_file:
            upload_folder = server.app.config['UPLOAD_FOLDER']
            user_image_file.save(f'{upload_folder}/{image_filename}')
        user_dao.save_user(user)
        return redirect(url_for('user_profile',pag='view'))