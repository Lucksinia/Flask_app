from typing import Dict

from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound
from blog import Author, Tag
from blog.forms.article import CreateArticleForm
from blog.models import Article, User
from blog.models.database import db

articles_app = Blueprint('articles_app', __name__, url_prefix='/articles', static_folder='../static')


@articles_app.route("/", endpoint="list")
def articles_list():
    articles = Article.query.all()
    users = User.query.all()
    authors = Author.query.all()
    return render_template('articles/list.html', articles=articles, users=users, authors=authors)


@articles_app.route('/<int:article_id>')
def get_article(article_id: int):
    article = Article.query.filter_by(id=article_id).options(joinedload(Article.tags)).one_or_none()  # подгружаем связанные теги!
    user = User.query.filter_by(id=article_id).one_or_none()
    print(article)
    try:
        if article is not None:
            return render_template('articles/details.html', article=article, user=user)
        else:
            raise KeyError
    except KeyError:
        raise NotFound(f'Article id {article_id} not found')


@articles_app.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)
    # добавляем доступные теги в форму
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]
    if request.method == "POST" and form.validate_on_submit():
        article = Article(title=form.title.data.strip(), text=form.text.data)
        db.session.add(article)
        if form.tags.data:  # если в форму были переданы теги (были выбраны)
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                article.tags.append(tag)  # добавляем выбранные теги к статье
        if current_user.author:
            # use existing author if present
            article.author = current_user.author
        else:
            # otherwise create author record
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            article.author = author
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create a new article!")
            error = "Could not create article!"
        else:
            return redirect(url_for("articles_app.get_article", article_id=article.id))
    return render_template("articles/create.html", form=form, error=error)

@articles_app.route("/data", endpoint="data")
def articles_data():
    import requests
    count_articles: Dict = requests.get('http://127.0.0.1:5000/api/articles/event_get_count/').json()
    url_articles = 'http://127.0.0.1:5000/api/articles/?include=author%2Ctags&fields%5Barticle%5D=id,title,text,' \
                   'dt_created,dt_updated,author,tags&fields%5Bauthor%5D=id,articles,user&fields%5Btag%5D=id,' \
                   'name&page%5Bnumber%5D=1&page%5Bsize%5D=10 '
    url_authors = 'http://127.0.0.1:5000/api/authors/?include=user%2Carticles&fields%5Bauthor%5D=id,user,' \
                  'articles&fields%5Buser%5D=last_name,email,first_name,username,author,id,' \
                  'is_staff&fields%5Barticle%5D=tags,text,title,dt_created,author,id,' \
                  'dt_updated&page%5Bnumber%5D=1&page%5Bsize%5D=10 '
    url_users = 'http://127.0.0.1:5000/api/users/?include=author&fields%5Buser%5D=id,first_name,last_name,username,' \
                'email,is_staff,author&fields%5Bauthor%5D=id,articles,user&page%5Bnumber%5D=1&page%5Bsize%5D=10 '
    r = requests.get(url_articles)
    result_articles = r.json()
    r = requests.get(url_users)
    result_users = r.json()
    r = requests.get(url_authors)
    result_authors = r.json()
    return render_template('articles/data.html', result_articles=result_articles, result_authors=result_authors, result_users=result_users, count_articles=count_articles)