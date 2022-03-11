# import requests
#
# url = 'https://raw.githubusercontent.com/kot-mechanic/mongodb_otus/main/screen/222222222222222222.png'
# r = requests.get(url, allow_redirects=True)
#
# open('D:\\work\\poslanie\\authservice\\ws_app\\tmp\\TestUser\\1.png', 'wb').write(r.content)

import time
# # from ws_app import db
# from ws_app.model.models import db, Authlog
#
#
# def create_auth_blueprint():
#     bp = Blueprint('auth', __name__)
#
#
#     controltime = int(time.time()) - 100
#     oldlogs = Authlog.query.filter_by(datetime<controltime).all()
#     for o in oldlogs:
#         db.session.delete(o)
#         db.session.commit()
#
#     return bp

print(int(time.time()))