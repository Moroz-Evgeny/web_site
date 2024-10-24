from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app.models import Articles
from app.translit import transliterate
articles_view = Blueprint('articles_view', __name__)


@articles_view.route('/articles_view-<userName>-<articleName>')
def article_view(userName, articleName):
  name_article = [i.title for i in Articles.query.filter_by(user_id=session['userId']).all()]
  for i in name_article:

    if transliterate(i) == articleName:
      article_html_content = Articles.query.filter_by(title=i, user_id=session['userId']).first().content
      return render_template('view_article.html', userName=userName, articleName=articleName, html_content=article_html_content, artName=i)