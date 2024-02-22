import os.path

from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, current_user, login_required, \
    logout_user
from werkzeug.utils import secure_filename

from data.db_session import global_init, create_session
from data.users import User
from data.articles import Article
from forms.edit_profile import EditProfileForm
from forms.login import LoginForm
from forms.register import RegisterForm
from forms.new_article import NewArticleForm

# ORM - Object-Relational Mapping

app = Flask(__name__)

app.config['SECRET_KEY'] = 'blablabla'
login_manager = LoginManager()
login_manager.init_app(app)

UPLOAD_FOLDER = os.getcwd() + '\\static\\img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
DEFAULT_IMAGE = 'default_image.png'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile(id):
    sess = create_session()
    user = sess.query(User).filter(User.id == id).first()

    context = {'title': 'Профиль', 'user': user,
               'default_user_avatar': DEFAULT_IMAGE}
    return render_template('profile.html', **context)


@app.route('/')
def index():
    sess = create_session()

    context = {'title': 'Главная', 'users': sess.query(User).all(),
               'default_user_avatar': DEFAULT_IMAGE}
    return render_template('index.html', **context)


@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    sess = create_session()
    user = sess.query(User).filter(User.id == id).first()
    sess.delete(user)
    sess.commit()
    return redirect('/')


@app.route('/about')
def about():
    return render_template('about.html', title='О Сайте')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        sess = create_session()
        user = sess.query(User).filter(email == User.email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect('/')
        else:
            return render_template('login.html', form=form,
                                   message='Неверные логин или пароль')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            return render_template('register.html', form=form,
                                   message='Пароли не совпадают')
        sess = create_session()
        if sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', form=form,
                                   message='Пользователь с такой почтой уже существует')
        user = User(email=form.email.data, name=form.name.data)
        user.set_password(form.password.data)
        sess.add(user)
        sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/create_article', methods=['POST', 'GET'])
@login_required
def create_article():
    form = NewArticleForm()
    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        form.image.data.save(UPLOAD_FOLDER + filename)
        a = Article(title=form.title.data, image=filename,
                    content=form.content.data)
        current_user.articles.append(a)
        sess = create_session()
        sess.merge(current_user)
        sess.commit()
        return redirect(f'/article/{a.id}')
    return render_template('new_article.html', form=form)

@app.route('/article/<int:article_id>')
def article(article_id):
    article = create_session().query(Article).filter(Article.id == article_id).first()
    return render_template('article.html', article=article)


@app.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    sess = create_session()
    user = sess.query(User).get(current_user.id)
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(UPLOAD_FOLDER + filename)
            user.image = filename
        user.name = form.name.data
        user.about = form.about.data
        sess.merge(user)
        sess.commit()
        return redirect(f'/profile/{current_user.id}')
    form.name.data = user.name
    form.about.data = user.about
    return render_template('edit_profile.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return create_session().query(User).get(user_id)


global_init('db/blogs.db')
app.run('127.0.0.1', 8080)
