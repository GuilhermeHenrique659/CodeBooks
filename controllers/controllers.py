from flask import flash, redirect, render_template, request, url_for
from config import server
from dao import UserDao
from models import User

user_dao = UserDao(server.db)

class ControllerLogin:
    def __init__(self) -> None:
        pass

    def index(self):
        return '<h1>CodeBooks</h1>'

    def login(self):
        return render_template('login.html')

    def authenticate(self):
        data = request.form
        user = user_dao.user_search_login(data['email'])
        if user:
            if user._password == data['password']:
                return redirect(url_for('index'))
            else:
                flash('senha errada')
                return redirect(url_for('login'))
        else:
            flash('usuario nao encontrado')
            return redirect(url_for('login'))

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