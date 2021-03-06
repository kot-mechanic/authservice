from flask import (
    Blueprint, request, jsonify
)

from flask_httpauth import HTTPBasicAuth
import time

auth = HTTPBasicAuth()
user = {'login': 'service', 'password': 'ScaNTestrApToWeITERaCEmanTALaver'}


@auth.verify_password
def verify_password(username, password):
    if username == user['login'] and password == user['password']:
        return username


def create_auth_blueprint():
    bp = Blueprint('auth', __name__)

    @bp.route('/login', methods=['POST'])
    @auth.login_required
    def login():
        from ws_app.model.models import db, Users, Authlog
        if not request.is_json:
            return jsonify({'error': 'Body is not json.', 'success': None}), 403
        json = request.get_json()
        user_name = json.get('nickname', None)
        ph = json.get('password', None)
        u = Users.query.filter_by(nickname=user_name, password=ph, active=True).first()
        ipaddr = request.remote_addr
        # print(ipaddr, user_name, ph, int(time.time()))
        if not u:
            log = Authlog(login=user_name, password=ph, ip=ipaddr, datetime=int(time.time()), succes=False)
            db.session.add(log)
            db.session.commit()
            return jsonify({'error': None, 'success': False}), 200
        else:
            log = Authlog(login=user_name, password=ph, ip=ipaddr, datetime=int(time.time()), succes=True)
            db.session.add(log)
            db.session.commit()
            return jsonify({'error': None, 'success': True}), 200



    return bp
