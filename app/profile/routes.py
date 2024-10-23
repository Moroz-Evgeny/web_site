import os
from flask import Blueprint, redirect, render_template, request, session, flash, url_for
from app.translit import transliterate
from app.models import Articles, User
from werkzeug.utils import secure_filename
from app.articles.routes import convert_image_to_base64
from app import db

profile = Blueprint('profile', __name__)

@profile.route('/profile/<userName>', methods=["GET", "POST"])
def profile_view(userName):
    if userName != session['userName'] or 'userName' not in session:
        flash('Доступ запрещён! Ошибка 403.')
        return render_template('profile.html')
    elif request.method == "POST":
        if 'photo' in request.files:
            file = request.files['photo']
            filename = secure_filename(file.filename)
            photo = os.path.join('uploads', filename)
            file.save(photo)
            conv_photo = convert_image_to_base64(photo)

            # Добавление фото в бд User
            user = User.query.get(session['userId'])
            user.photo = conv_photo
            db.session.commit()

        user_photo = User.query.filter_by(email=session['userEmail']).first().photo
        return redirect(url_for('profile.profile_view', userName=session['userName']))
    else:         
        name_trans_article = [transliterate(i.title) for i in Articles.query.filter_by(user_id=session['userId']).all()]
        name_article = [i.title for i in Articles.query.filter_by(user_id=session['userId']).all()]
        user_photo = User.query.filter_by(email=session['userEmail']).first().photo
        return render_template('profile.html', userFirstname=session['userFirstname'], userLastname=session['userLastname'], userEmail=session['userEmail'], userName=session['userName'], userId = session['userId'], name_trans_article=name_trans_article, name_article=name_article, len_art=len(name_article), userPhoto=user_photo)
