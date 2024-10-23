import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.urandom(24)
    
    db.init_app(app)

    # Регистрация Blueprints
    from app.auth.routes import auth
    from app.profile.routes import profile
    from app.articles.routes import articles
    from app.views import main
    from app.articles_view.routes import articles_view

    app.register_blueprint(articles_view)
    app.register_blueprint(auth)
    app.register_blueprint(profile)
    app.register_blueprint(articles)
    app.register_blueprint(main)

    return app
