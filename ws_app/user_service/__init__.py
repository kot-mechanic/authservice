import os
import time
import requests

from flask import (
    Blueprint, request, jsonify, send_file
)
from werkzeug.utils import secure_filename

from ws_app.auth import auth


def create_users_blueprint(db, upload_path):
    bp = Blueprint('users', __name__)

    @bp.route('/', methods=['POST', 'GET'])
    @auth.login_required
    def users():
        from ws_app.model.models import Users
        from ws_app.model.models import Socnet
        if request.method == 'POST':
            if not request.is_json:
                return jsonify({'error': 'Body is not json.', 'success': None}), 403
            json = request.get_json()
            json['reg_date'] = int(time.time())
            u = Users.from_json(json)
            if 'socnet' in json:
                for item in json['socnet']:
                    json_socnet = item
                u.socnet.append(Socnet.from_json(json_socnet))
            if 'socnet' not in json:
                u.socnet.append(Socnet())
            try:
                # print('Пытаюсь записать в БД')
                db.session.add(u)
                db.session.commit()
            except Exception as e:
                # print('Не удалось записать в БД')
                return jsonify({'error': 'An user with a same nickname exists.', 'success': None}), 403
            return jsonify(u.to_dict()), 200
        else:
            return jsonify([u.to_dict() for u in Users.query.all()]), 200

    @bp.route('/<user_nickname>', methods=['POST', 'GET', 'DELETE'])
    @auth.login_required
    def user(user_nickname):
        from ws_app.model.models import Users
        from ws_app.model.models import Socnet
        u = Users.query.filter_by(nickname=user_nickname)
        u1 = Users.query.filter_by(nickname=user_nickname).first()
        if not u.first():
            return jsonify({'error': 'User not found.', 'success': None}), 404
        if request.method == 'DELETE':
            for s in u.first().socnet:
                db.session.delete(s)
            for p in u.first().pics:
                db.session.delete(p)
                try:
                    os.remove('%s/%s/%s' % (upload_path, user_nickname, p.filepath))
                except:
                    pass
            result = u.delete()
            db.session.commit()
            return jsonify({'error': None, 'success': result}), 200
        if request.method == 'POST':
            if not request.is_json:
                return jsonify({'error': 'Body is not json.', 'success': None}), 403
            json = request.get_json()
            if 'active' in json:
                json['delete_date'] = int(time.time())
            if 'socnet' in json:
                for item in json['socnet']:
                    json_socnet = item
                    socnet = Socnet.query.filter_by(user_id=u1.user_id)
                    del json['socnet']
                    socnet.update(json_socnet)
            u.update(json)
            db.session.commit()
            return jsonify(u.first().to_dict()), 200
        else:
            return jsonify(u.first().to_dict()), 200

    @bp.route('/<user_nickname>/socnet', methods=['POST', 'GET'])
    @auth.login_required
    def user_socnet(user_nickname):
        from ws_app.model.models import Users
        from ws_app.model.models import Socnet
        u = Users.query.filter_by(nickname=user_nickname).first()
        if not u:
            return jsonify({'error': 'User not found.', 'success': None}), 404
        if request.method == 'POST':
            if not request.is_json:
                return jsonify({'error': 'Body is not json.', 'success': None}), 403
            json = request.get_json()
            socnet = Socnet.query.filter_by(user_id=u.user_id)
            socnet.update(json)
            db.session.commit()
            return jsonify(socnet.first().to_dict()), 200
        else:
            socnet = u.socnet
            if socnet:
                return jsonify(socnet[0].to_dict()), 200
            return jsonify({}), 200

    @bp.route('/pic', methods=['POST', 'DELETE'])
    @auth.login_required
    def pic_from_url():
        from ws_app.model.models import Users
        from ws_app.model.models import Pic
        if request.method == 'POST':
            if not request.is_json:
                return jsonify({'error': 'Body is not json.', 'success': None}), 403
            json = request.get_json()
            r = requests.get(json['pic_url'], allow_redirects=True)
            # print(r.headers)
            # print(r.headers['Content-Type'])
            filename = secure_filename('%s_' % int(time.time()))+'.jpg'
            full_path = '%s/%s/' % (upload_path, json['nickname'])
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            open(full_path+'\\'+filename, 'wb').write(r.content)
            u = Users.query.filter_by(nickname=json['nickname']).first()
            p = Pic(user_id=u.user_id, filepath=filename, ava=False)
            db.session.add(p)
            db.session.commit()
            return jsonify(p.to_dict()), 200


    @bp.route('/<user_nickname>/pics', methods=['POST', 'GET'])
    @auth.login_required
    def user_pics(user_nickname):
        from ws_app.model.models import Users
        from ws_app.model.models import Pic
        u = Users.query.filter_by(nickname=user_nickname).first()
        if not u:
            return jsonify({'error': 'User not found.', 'success': None}), 404
        pics = Pic.query.filter_by(user_id=u.user_id).all()
        if request.method == 'POST':
            try:
                pic_id = int(request.args.get('pic_id'))
            except:
                return jsonify({'error': "A pic_id parameter must be integer.", 'success': False}), 404
            for p in pics:
                p.ava = True if p.pic_id == pic_id else False
                db.session.add(p)
                db.session.commit()
            return jsonify([p.to_dict() for p in Pic.query.filter_by(user_id=u.user_id).all()]), 200
        return jsonify([p.to_dict() for p in pics]), 404

    @bp.route('/<user_nickname>/pic', methods=['POST', 'GET', 'DELETE', 'PUT'])
    @auth.login_required
    def user_pic(user_nickname):
        from ws_app.model.models import Users
        from ws_app.model.models import Pic
        filename_arg = request.args.get('filename')
        u = Users.query.filter_by(nickname=user_nickname).first()
        if not u:
            return jsonify({'error': 'User not found.', 'success': None}), 404
        if request.method == 'DELETE':
            if not filename_arg:
                return jsonify({'error': 'File not found.', 'success': None}), 404
            pics = Pic.query.filter_by(user_id=u.user_id, filepath=filename_arg).all()
            for p in pics:
                db.session.delete(p)
                db.session.commit()
            try:
                os.remove('%s/%s/%s' % (upload_path, user_nickname, filename_arg))
            except FileNotFoundError:
                return jsonify({'error': 'File not found.', 'success': None}), 404
            return jsonify({'error': None, 'success': len(pics)}), 200
        if request.method == 'POST':
            try:
                f = request.files['file']
            except Exception as e:
                return jsonify({'error': e, 'success': None}), 404
            if not allowed_file(f.filename):
                return jsonify({'error': 'File extension is not allowed.', 'success': None}), 404
            filename = secure_filename('%s_' % int(time.time()) + f.filename)
            full_path = '%s/%s/' % (upload_path, user_nickname)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            f.save(os.path.join(full_path, filename))
            p = Pic(user_id=u.user_id, filepath=filename, ava=False)
            db.session.add(p)
            db.session.commit()
            return jsonify(p.to_dict()), 200
        else:
            if not filename_arg:
                return jsonify({'error': 'File not found.', 'success': None}), 404
            try:
                return send_file('%s/%s/%s' % (upload_path, user_nickname, filename_arg),
                                 mimetype='image/%s' % get_file_extension(filename_arg))
            except FileNotFoundError:
                return jsonify({'error': 'File not found.', 'success': None}), 404

    @bp.route('/authlog/<user_nickname>', methods=['GET'])
    @auth.login_required
    def get_authlog(user_nickname):
        from ws_app.model.models import Authlog
        log = Authlog.query.filter_by(login=user_nickname).all()
        if not log:
            return jsonify({'error': 'Log not found.', 'success': None}), 404
        return jsonify([l.to_dict() for l in log]), 200


    def allowed_file(filename):
        from ws_app import ALLOWED_EXTENSIONS
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def get_file_extension(filename):
        return os.path.splitext(filename)[1].replace('.', '')

    return bp
