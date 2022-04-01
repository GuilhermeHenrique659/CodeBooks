from flask import flash, redirect, render_template, request, url_for, session
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
                return redirect(url_for('index'))
            else:
                flash('senha errada')
                return redirect(url_for(data['url']))
        else:
            flash('usuario nao encontrado')
            return redirect(url_for(data['url']))

    def logout(self):
        session['login_user'] = None
        return redirect(url_for('login'))

class ControllerRegister:
    def __init__(self) -> None:
        pass

    def register(self):
        return render_template('register.html')

    def sing_in(self):
        data = request.form
        user = User(data['name'],data['email'],data['password'])
        result = user_dao.create_user(user)
        if result == 1062:
            flash('email ja ultilizado')
            return redirect(url_for('register'))
        else:
            return redirect(url_for('login'))