from flask import Blueprint, render_template, session, flash, redirect, url_for
from app import db
from app.models import User, Articles
from app import translit

main = Blueprint('main', __name__)

@main.route('/')
def index():
    try:
        return render_template('index.html', userName=session['userName'], userLogged='userLogged' in session)
    except KeyError:
        return render_template('index.html')

# Обработка ошибки 403
@main.errorhandler(403)
def forbidden_error(error):
    flash('Доступ запрещён! Ошибка 403.')
    return render_template('index.html')

# Создание контекста для доступа к категориям
@main.app_context_processor
def inject_categories():
    categories = [
        "Гуманитарные науки", "Естественные науки", "Точные науки", "Постнаука",
        "Биология", "История", "Социальные науки", "Культура", "Медицина",
        "Физика", "Психология", "Когнитивные науки", "Технологии", "Книги",
        "Животный мир", "Новости", "Игры", "Зарубежная литература", "Новости Ростова-на-дону"
    ]
    trans_categories = [translit.transliterate(category) for category in categories]
    return dict(categories=categories, trans_categories=trans_categories)
