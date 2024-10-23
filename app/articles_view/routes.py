from flask import Blueprint, render_template, redirect, url_for, session, request, flash


articles_view = Blueprint('articles_view', __name__)


@articles_view.route('/articles_view-<userName>-<articleName>')
def article_view(userName, articleName):
  return render_template('view_article.html', userName=userName, articleName=articleName)