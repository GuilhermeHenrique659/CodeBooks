from flask import jsonify, session
from factoryDao import dao

class ControllerNotification:
    def find_all(self):
        notifications_list:list = dao.notification.find_all(session['user_id'])
        return jsonify([notification.__dict__ for notification in notifications_list]),200