from flask import render_template,redirect, request,session,url_for
from factoryDao import dao
from config import server
from models import Code

class ControllerCode:
    def __init__(self) -> None:
        pass
    def code_list(self, id):
        list_code = dao.code.find_all_by_post(id)
        listComment = dao.comment.find_all_by_post(id)
        return render_template('code.html', list_code = list_code,post_id=id, listComment = listComment)
    
    @server.loggin_required
    def add_code(self,id):
        data_code_front = request.form
        code = Code(data_code_front['code'],id,session['user_id'])
        dao.code.store(code)
        return redirect(url_for('post',id=id))

    @server.loggin_required
    def delete_code(self, id):
        post = request.args['post_id']
        dao.code.delete(id,session['user_id'])
        return redirect(url_for('post',id=post))
