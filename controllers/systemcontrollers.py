from flask import flash, redirect, render_template, request, send_from_directory, url_for, session
from config import server
from factoryDao import dao
from models import User


class ControllerLogin:
    def __init__(self) -> None:
        pass

    def login(self):
        return render_template('login.html')
 
    def authenticate(self):
        data = request.form
        user = dao.user.user_search_login(data['email'])
        if user:
            if user._password == data['password']:
                session['login_user'] = data['email']
                session['user_id'] = user._id
                session['user_name'] = user._name
                return redirect(url_for('index'))
            else:
                flash('senha errada')
                return redirect(url_for(request.args['previous']))
        else:
            flash('usuario nao encontrado')
            return redirect(url_for(request.args['previous']))

    @server.loggin_required
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
        result = dao.user.save_user(user)
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