from click import edit
from flask import render_template,request,redirect, session,url_for
from config import server
from dao import UserDao 
user_dao = UserDao(server.db)
class ControllerUser:
    def __init__(self) -> None:
        pass
    def user_profile(self):
        if 'login_user' not in session or session['login_user'] == None:
            return redirect(url_for('login'))
        User_profile = user_dao.search_user_profile(session['user_id'])
        if(request.args['pag'] == 'edit'):
            return render_template('profile_edit.html', user_profile = User_profile )

        else:
            return render_template('profile.html', user_profile = User_profile )