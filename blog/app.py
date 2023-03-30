from combojsonapi.event import EventPlugin
from flask_login import LoginManager
from flask_migrate import Migrate
from flask import Flask, session
from flask_wtf import CSRFProtect
from blog import User
from blog.admin.views import admin
from blog.articles.views import articles_app
from blog.auth.views import auth_app
from blog.authors.views import authors_app
from blog.models.database import db
from blog.security import flask_bcrypt
from combojsonapi.spec import ApiSpecPlugin
import os
from flask_combo_jsonapi import Api
from combojsonapi.permission import PermissionPlugin


csrf = CSRFProtect()

login_manager = LoginManager()
migrate = Migrate()
api = Api()

def create_app() -> Flask:
    print('start!')
    app = Flask(__name__)
    app.config.from_object('blog.config')
    register_extensions(app)
    register_blueprints(app)
    create_init_user(app)
    register_api()
    # create_articles(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    csrf.init_app(app)
    admin.init_app(app)

    flask_bcrypt.init_app(app)
    event_plugin = EventPlugin()
    permission_plugin = PermissionPlugin(strict=False)
    api.plugins = [
        event_plugin,
        permission_plugin,
        ApiSpecPlugin(
            app=app,
            tags={
                'Tag': 'Tag API',
                'User': 'User API',
                'Author': 'Author API',
                'Article': 'Article API',
            }
        ),
    ]

    api.init_app(app)
    login_manager.login_view = 'auth_app.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_api():
    from blog.api.tag import TagList
    from blog.api.tag import TagDetail
    from blog.api.user import UserList
    from blog.api.user import UserDetail
    from blog.api.author import AuthorList
    from blog.api.author import AuthorDetail
    from blog.api.article import ArticleList
    from blog.api.article import ArticleDetail

    api.route(TagList, 'tag_list', '/api/tags/', tag='Tag')
    api.route(TagDetail, 'tag_detail', '/api/tags/<int:id>', tag='Tag')

    api.route(UserList, "user_list", "/api/users/", tag="User")
    api.route(UserDetail, "user_detail", "/api/users/<int:id>/", tag="User")

    api.route(AuthorList, "author_list", "/api/authors/", tag="Author")
    api.route(AuthorDetail, "author_detail", "/api/authors/<int:id>/", tag="Author")

    api.route(ArticleList, 'article_list', '/api/articles/', tag='Article')
    api.route(ArticleDetail, 'article_detail', '/api/articles/<int:id>', tag='Article')

def register_blueprints(app: Flask):
    app.register_blueprint(auth_app, url_prefix='/auth')

    app.register_blueprint(articles_app)
    app.register_blueprint(authors_app, url_prefix="/authors")


def create_init_user(app):
    from blog.models import User
    print('starting create users...')
    with app.app_context():
        db.create_all()
        if db.session.query(User).filter_by(username='admin').count() < 1:
            admin = User(first_name='Konstantin', last_name='Suchkov', username="admin", is_staff=True,
                         email='konstantinsuchkov@yandex.ru', password='123')
            db.session.add(admin)
        if db.session.query(User).filter_by(username='Amelka').count() < 1:
            amelia = User(first_name='Amelia', last_name='Suchkova', username="Amelka", is_staff=False,
                          email='amelia@yandex.ru', password='123')
            db.session.add(amelia)
        if db.session.query(User).filter_by(username='Varvarka').count() < 1:
            varvara = User(first_name='Varvara', last_name='Suchkova', username="Varvarka", is_staff=False,
                           img='varvarka.png', email='varya@yandex.ru', password='123')
            db.session.add(varvara)
        db.session.commit()
        print('done!')

