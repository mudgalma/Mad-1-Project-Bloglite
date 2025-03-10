from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import urllib.request
import os 
from werkzeug.utils import secure_filename
db = SQLAlchemy()

DB_NAME = "database.db"
UPLOAD_FOLDER='website/static/'
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY']="jhgfgds"
    # configure the SQLite database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    # initialize the app with the extension
    app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH']=16*1024*1024

    
 
    

    db.init_app(app)
    from.views import views
    from.auth import auth
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    from.models import User,Blog,Followers,Comment
    create_database(app)
    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app
def create_database(app):
    if not path.exists('website/'+ DB_NAME):
        with app.app_context():
            db.create_all()
        print('created')

    