from flask import render_template,redirect,session,url_for

class ControllerFeed:
    def __init__(self) -> None:
        pass

    def index(self):
        if 'login_user' not in session or session['login_user'] == None:
            pass
        return render_template('base.html')