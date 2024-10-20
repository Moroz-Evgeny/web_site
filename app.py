from flask import Flask, flash, redirect, render_template, session, url_for, request
from flask_sqlalchemy import SQLAlchemy
import translit

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'ofjoiejj4983f4398j9f092k0k0ef0ejf093'



print('soidjfoisdjofidjsoifj')

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<User {self.id}>'


# Главная страница
@app.route('/')
def index():
    try:
        return render_template('index.html', userName = session['userName'], userLogged = 'userLogged' in session)
    except:
        return render_template('index.html')
    
# Маршрут для логина
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['emailLogin']
        password = request.form['passwordLogin']

        # Поиск пользователя по email и паролю
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['userFirstname'] = user.name
            session['userLastname'] = user.last_name
            session['userEmail'] = user.email
            session['userLogged'] = True
            session['userName'] = translit.transliterate(user.name + '_' + user.last_name)
            return redirect(url_for('index', userName = session['userName'], userLogged = 'userLogged' in session))
        else:
            # Если пользователь не найден, возвращаем на страницу с ошибкой
            flash('Неверный логин или пароль, повторите попытку')
            return redirect(url_for('login'))
    else:
        return render_template('reg_log.html')

# Маршрут для регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['emailRegister']
        password = request.form['passwordRegister']

        # Проверка, существует ли пользователь с таким email
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Пользователь с таким Email уже существует')
            return render_template('reg_log.html')
        
        # Создание нового пользователя
        new_user = User(name=name, last_name=last_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрированы, авторизуйтесь!', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('reg_log.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index')) 

@app.route('/profile/<userName>')
def profile(userName):
    if userName != session['userName'] or 'userName' not in session:
        flash('Доступ запрещён! Ошибка 403.')
        return render_template('profile.html')
    else:
        return render_template('profile.html', userFirstname=session['userFirstname'], userLastname=session['userLastname'], userEmail=session['userEmail'])
        

if __name__ == "__main__":
    # Создание всех таблиц при запуске
    with app.app_context():
        db.create_all()
    app.run(debug=True)

