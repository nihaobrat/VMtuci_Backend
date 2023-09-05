from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Здесь можно добавить проверку логина и пароля
        # Если все верно, перенаправляем пользователя, например, на главную страницу (или другую страницу вашего выбора)
        return "Успешный вход!"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        dob = request.form.get('dob')
        password = request.form.get('password')
        password_repeat = request.form.get('password-repeat')

        # Проверка пароля
        if password != password_repeat:
            return "Пароли не совпадают"

        # Перенаправляем на страницу входа после успешной регистрации
        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)


