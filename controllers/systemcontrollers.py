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
        user:User = dao.user.find_by_email(data['email'])
        if user:
            if user._password == data['password']:
                session['login_user'] = data['email']
                session['user_id'] = user._id
                session['user_name'] = user._name
                session['user_image'] = user.image
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
        try:
            dao.user.store(user)
            return redirect(url_for('login'))
        except Exception:
            flash("Email ou usuario nao disponivel")
            return redirect(url_for('register'))
            


class ControllerUploads:
    def __init__(self) -> None:
        pass

    def upload_folder(self,filename):
        return send_from_directory('uploads',filename)