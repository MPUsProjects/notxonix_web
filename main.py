from flask import Flask, render_template, redirect, request, make_response, session, abort, jsonify
from assets.data import db_session
from assets.data.users import *
from assets.data.news import *
from assets.data.game_data import NotxonixData
from assets.data import api_resources
from assets.forms.user import RegisterForm, LoginForm
from assets.forms.news import NewsForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
night = False
day = False
# проверка времени
timenow = datetime.datetime.now().hour
if timenow >= 21 or timenow < 7:
    night = True
else:
    day = True


# загрузка пользователя из бд
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# загрузка новостей
def main():
    db_session.global_init("assets/db/data.db")

    api.add_resource(api_resources.LoginResource, '/loginapi')
    api.add_resource(api_resources.NotxonixResource, '/api/notxonix')

    app.run()


# ответвление для создания новостей
@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News)
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    if day:
        return render_template("index_day.html", news=news)
    else:
        return render_template("index_night.html", news=news)

# Ошибки
@app.errorhandler(404)
def er404(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


# API
pass


@app.route('/api/login', methods=['GET', 'POST'])
def api_handler():
    pass

# Вкладки
# вкладка регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            if day:
                return render_template('register_day.html', title='Регистрация',
                                        form=form,
                                        message="Пароли не совпадают")
            elif night:
                return render_template('register_night.html', title='Регистрация',
                                        form=form,
                                        message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            if day:
                return render_template('register_day.html', title='Регистрация',
                                        form=form,
                                        message="Такой пользователь уже есть")
            elif night:
                return render_template('register_night.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()

        acc = db_sess.query(User).filter(User.email == form.email.data).first()
        userident = UserIdentifier(
            name=acc.name,
            userid=acc.id
        )
        db_sess.add(userident)
        db_sess.commit()
        return redirect('/login')
    if day:
        return render_template('register_day.html', title='Регистрация', form=form)
    elif night:
        return render_template('register_night.html', title='Регистрация', form=form)


# проверка куки, отдельная вкладка на кол-во раз
@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


# тест сессии
@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


# вкладка входа в аккаунт
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        if day:
            return render_template('login_day.html',
                                    message="Неправильный логин или пароль",
                                    form=form)
        elif night:
            return render_template('login_night.html',
                                    message="Неправильный логин или пароль",
                                    form=form)
    if day:
        return render_template('login_day.html', title='Авторизация', form=form)
    elif night:
        return render_template('login_night.html', title='Авторизация', form=form)


# активация выхода из аккаунта
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# добавление новости
@app.route('/news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    if day:
        return render_template('news_day.html', title='Добавление новости',
                                form=form)
    else:
        return render_template('news_night.html', title='Добавление новости',
                               form=form)


# изменение конкретной новости
@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    if day:
        return render_template('news_day.html',
                                title='Редактирование новости',
                                form=form
                                )
    else:
        return render_template('news_night.html',
                               title='Редактирование новости',
                               form=form
                               )

# удаление конкретной новости
@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


if __name__ == '__main__':
    main()
