from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ws_app.auth import create_auth_blueprint
from ws_app.user_service import create_users_blueprint

db = SQLAlchemy()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://users:xNMqdMcGdPWhMKrc7P31@192.168.42.101/users'
    app.config['UPLOAD_FOLDER'] = '/opt/ws_app/tmp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(create_auth_blueprint(), url_prefix='/api/v1/auth')
    app.register_blueprint(create_users_blueprint(db, app.config['UPLOAD_FOLDER']), url_prefix='/api/v1/users')

    return app
