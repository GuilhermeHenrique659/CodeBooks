from flask import render_template,redirect,session,url_for
from dao import CodeDao
from config import server
code_dao = CodeDao(server.db)
class CodeController:
    def __init__(self) -> None:
        pass
    def code_list(self, id):
        list_code = code_dao.list_code(id)
        return render_template('code.html', list_code = list_code)
    