from flask import Blueprint, flash, redirect, render_template, session, url_for, request
from app.models import User
from app import db
from app import translit
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['emailLogin']
        password = request.form['passwordLogin']

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['userId'] = user.id
            session['userFirstname'] = user.name
            session['userLastname'] = user.last_name
            session['userEmail'] = user.email
            session['userLogged'] = True
            session['userName'] = translit.transliterate(user.name + '_' + user.last_name)
            return redirect(url_for('main.index'))
        else:
            flash('Неверный логин или пароль, повторите попытку')
            return redirect(url_for('auth.login'))
    return render_template('reg_log.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['emailRegister']
        password = request.form['passwordRegister']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Пользователь с таким Email уже существует')
            return render_template('reg_log.html')

        new_user = User(name=name, last_name=last_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрированы, авторизуйтесь!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reg_log.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
