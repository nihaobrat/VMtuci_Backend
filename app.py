from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {}
posts = []

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('glavpage.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        login = request.form['login']
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']

        # Обрабатываем загрузку аватара
        avatar = request.files.get('avatar')
        if avatar:
            avatar_filename = secure_filename(avatar.filename)
            avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename)
            avatar.save(avatar_path)
        else:
            avatar_filename = 'default.png' # Или другое изображение по умолчанию

        # Проверяем, занят ли логин
        if login in users:
            return "Логин уже занят", 400

        # Сохраняем информацию о пользователе, включая путь к аватару
        users[login] = {
            'login': login,
            'name': name,
            'surname': surname,
            'email': email,
            'password': password,
            'avatar': avatar_filename
        }

        session['user'] = login
        return redirect(url_for('lenta'))

    return render_template('registration.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        user = users.get(login)
        if user and user['password'] == password:
            # Успешный вход
            session['user'] = login
            return redirect(url_for('lenta'))

        else:
            return "Неверный логин или пароль", 401

    return render_template('signin.html')

@app.route('/lenta')
def lenta():
    if 'user' not in session:
        return redirect(url_for('signin'))

    user_login = session['user']
    user_data = users.get(user_login, {})
    user_avatar_path = 'uploads/' + user_data.get('avatar', 'default.png')  # 'default.png' - изображение по умолчанию
    return render_template('lenta.html', posts=posts, user_data=user_data, user_avatar_path=user_avatar_path)


@app.route('/notifications')
def notifications():

    return render_template('notifications.html')



@app.route('/user_settings', methods=['GET', 'POST'])
def user_settings():
    if 'user' not in session:
        return redirect(url_for('signin'))

    user_login = session['user']
    user_data = users.get(user_login)

    if request.method == 'POST':
        # Update user_data based on form input
        user_data['name'] = request.form.get('first-name')
        user_data['surname'] = request.form.get('last-name')
        user_data['nickname'] = request.form.get('nickname')
        user_data['birthdate'] = request.form.get('birthdate')
        user_data['gender'] = request.form.get('gender')
        user_data['email'] = request.form.get('email')
        user_data['password'] = request.form.get('password')
        user_data['country'] = request.form.get('country')

        # Update the user entry in the users dictionary
        users[user_login] = user_data

        # Redirect to the 'lenta' page after updating
        return redirect(url_for('lenta'))

    return render_template('user_settings.html', user_data=user_data)

    return render_template('user_settings.html', user_data=user_data)


@app.route('/createpost', methods=['GET', 'POST'])
def create_post():
    if 'user' not in session:
        return redirect(url_for('signin'))

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.files.get('image')

        if image:
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)
        else:
            image_filename = 'default.png'  # Или другое изображение по умолчанию

        post = {
            'author': users[session['user']]['name'],  # Предполагаем, что 'name' есть в данных пользователя
            'title': title,
            'content': content,
            'image_filename': image_filename,
            'timestamp': datetime.utcnow()  # Сохраняем текущее время
        }
        posts.append(post)
        return redirect(url_for('lenta'))

    return render_template('createpost.html')



@app.route('/deletepost/<int:post_index>', methods=['POST'])
def delete_post(post_index):
    if 'user' not in session:
        return redirect(url_for('signin'))

    # Проверяем, существует ли пост с таким индексом
    if post_index < len(posts):
        del posts[post_index]
        # Можно добавить сообщение об успешном удалении
    else:
        # Можно добавить сообщение об ошибке, если пост не найден
        pass

    return redirect(url_for('lenta'))


@app.route('/allusers')
def all_users():
    if 'user' not in session:
        return redirect(url_for('signin'))

    return render_template('allusers.html', users=users, current_user=session['user'])


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('registration'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
