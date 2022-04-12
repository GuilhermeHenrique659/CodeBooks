from flask import flash, redirect, render_template, request, send_from_directory, url_for, session
from config import server
from dao import UserDao
from models import User

user_dao = UserDao(server.db)


class ControllerLogin:
    def __init__(self) -> None:
        pass

    def login(self):
        return render_template('login.html')

    def authenticate(self):
        data = request.form
        user = user_dao.user_search_login(data['email'])
        if user:
            if user._password == data['password']:
                session['login_user'] = data['email']
                session['username'] = user._name
                session['user_id'] = user._id
                session['user_img'] = user._image
                return redirect(url_for('index'))
            else:
                flash('senha errada')
                return redirect(url_for(request.args['previous']))
        else:
            flash('usuario nao encontrado')
            return redirect(url_for(request.args['previous']))

    def logout(self):
        session['login_user'] = None
        session.clear()
        return redirect(url_for('login'))

class ControllerRegister:
    def __init__(self) -> None:
        pass

    def register(self):
        return render_template('register.html')

    def sing_in(self):
        data = request.form
        user = User(data['name'],data['email'],data['password'])
        result = user_dao.save_user(user)
        if result == "email not available":
            flash('email ja ultilizado')
            return redirect(url_for('register'))
        else:
            return redirect(url_for('login'))

class ControllerUploads:
    def __init__(self) -> None:
        pass

    def upload_folder(self,filename):
        return send_from_directory('uploads',filename)