import os
from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app.models import Articles, Categories
from app import db
from app import translit

articles = Blueprint('articles', __name__)

categories = ["Гуманитарные науки", "Естественные науки", "Точные науки", "Постнаука", "Биология", "История", "Социальные науки", "Культура", "Медицина", "Физика", "Психология", "Когнитивные науки", "Технологии", "Книги", "Животный мир", "Новости", "Игры", "Зарубежная литература", "Новости Ростова-на-дону"]
trans_categories = [translit.transliterate(i) for i in categories]


@articles.route('/new-article', methods=["GET", "POST"])
def new_article():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content'] 
        category = [Categories.query.filter_by(name=request.form.get(f'category{i}')).first().id for i in range(1, 4) if request.form.get(f'category{i}')]

        # Обработка загрузки картинки
        if 'cover' in request.files:
            cover_file = request.files['cover']
            if cover_file.filename != '':
                # Сохраняем файл в папку uploads (создайте эту папку в корне вашего проекта)
                upload_folder = 'uploads'
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                
                cover_path = os.path.join(upload_folder, cover_file.filename)
                cover_file.save(cover_path)
                cover = cover_path

        # Получаем user_id из сессии или устанавливаем в None
        user_id = session.get('userId')

        # Создание новой статьи
        article = Articles(title=title, content=content, cover=cover, user_id=user_id, categories=category)

        db.session.add(article)
        db.session.commit()

        flash('Статья успешно добавлена!', 'success')
        return redirect(url_for('main.index'))
    else:
        if not session.get('userLogged'):
            flash('Войдите или зарегистрируйтесь!')
            return redirect(url_for('main.index'))
        else:
            return render_template('new_article.html', cat=categories, trans_cat=trans_categories)