from flask import render_template,redirect, request,session,url_for
from dao import CodeDao
from config import server
from models import Code

code_dao = CodeDao(server.db)

class CodeController:
    def __init__(self) -> None:
        pass
    def code_list(self, id):
        list_code = code_dao.list_code(id)
        
        return render_template('code.html', list_code = list_code,post_id=id)
    
    @server.loggin_required
    def add_code(self,id):
        data_code_front = request.form
        code = Code(data_code_front['code'],id,session['user_id'])
        code_dao.create_code(code)
        return redirect(url_for('post',id=id))