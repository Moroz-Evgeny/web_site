from flask import Blueprint, render_template, session, flash

profile = Blueprint('profile', __name__)

@profile.route('/profile/<userName>')
def profile_view(userName):
    if userName != session['userName'] or 'userName' not in session:
        flash('Доступ запрещён! Ошибка 403.')
        return render_template('profile.html')
    return render_template('profile.html', userFirstname=session['userFirstname'], userLastname=session['userLastname'], userEmail=session['userEmail'])
