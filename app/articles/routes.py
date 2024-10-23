import base64, json, os, mammoth, win32com.client
from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app.models import Articles, Categories
from app import db
from app import translit
from werkzeug.utils import secure_filename

articles = Blueprint('articles', __name__)

categories = ["Гуманитарные науки", "Естественные науки", "Точные науки", "Постнаука", "Биология", "История", "Социальные науки", "Культура", "Медицина", "Физика", "Психология", "Когнитивные науки", "Технологии", "Книги", "Животный мир", "Новости", "Игры", "Зарубежная литература", "Новости Ростова-на-дону"]
trans_categories = [translit.transliterate(i) for i in categories]

ALLOWED_EXTENSIONS = {'docx'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_image_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')



@articles.route('/new-article', methods=["GET", "POST"])
def new_article():
    # for i in trans_categories:
    #     cat = Categories(name = i)
    #     db.session.add(cat)
    # db.session.commit()

    if request.method == "POST":
        title = request.form['title'] 
        category_ids = [
        Categories.query.filter_by(name=request.form.get(f'category{i}')).first().id
        for i in range(1, 4)
        if request.form.get(f'category{i}') and Categories.query.filter_by(name=request.form.get(f'category{i}')).first()
        ]
        
        # Преобразуем список ID категорий в JSON
        category = json.dumps(category_ids)

        # Обработка загрузки картинки
        if 'cover' and 'word_file' in request.files:
            cover_file = request.files['cover']
            if cover_file.filename != '':
                # Сохраняем файл в папку uploads (создайте эту папку в корне вашего проекта)
                upload_folder = 'uploads'
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                
                cover_path = os.path.join(upload_folder, cover_file.filename)
                cover_file.save(cover_path)
                cover = convert_image_to_base64(cover_path)
            # Обработка загрузги статьи        
            file = request.files['word_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_folder, filename))

                    # Конвертация docx в html
                with open(os.path.join(upload_folder, filename), "rb") as docx_file:
                    result = mammoth.convert_to_html(docx_file)
                    html_content = result.value  # Конвертированный HTML

                # Получаем user_id из сессии или устанавливаем в None
                user_id = session.get('userId')

                # Создание новой статьи
                article = Articles(title=title, content=html_content, cover=cover, user_id=user_id, categories=category)

                db.session.add(article)
                db.session.commit()

                article_id = article.id

                # Добавление в таблицу категорий id статьи
                for category_id in category:
                    category = Categories.query.get(category_id)
                    
                    if category:
                        # Десериализуем список ID статей (если уже есть)
                        if category.id_article:
                            id_article_list = json.loads(category.id_article)
                        else:
                            id_article_list = []

                        # Добавляем новый ID статьи в список
                        id_article_list.append(article_id)

                        # Сериализуем список обратно в строку и сохраняем
                        category.id_article = json.dumps(id_article_list)

                        # Сохраняем изменения в базе данных
                        db.session.commit()

                flash('Статья успешно добавлена!', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Файл должен быть с расширением docx')
                return redirect(url_for('articles.new_article'))            
            


           


    else:
        if not session.get('userLogged'):
            flash('Войдите или зарегистрируйтесь!')
            return redirect(url_for('main.index'))
        else:
            return render_template('new_article.html', cat=categories, trans_cat=trans_categories)