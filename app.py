from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'q8X2WzySJCbt#cY4errG63xl*M7A~$u$G*01'

# Функция для получения соединения с базой данных
def get_db_connection():
    conn = sqlite3.connect('anime_movies.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM movies ORDER BY RANDOM()').fetchall()
    conn.close()
    return render_template('index.html', movies=movies)

@app.route('/watch/<int:movie_id>')
def watch(movie_id):
    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()
    conn.close()
    if movie is not None:
        return render_template('watch.html', movie=movie)
    else:
        return redirect(url_for('index'))

# Функция для проверки пароля (для простоты, пароль хранится в коде)
def check_admin_password(password):
    admin_password_hash = 'scrypt:32768:8:1$XB7ZdR7608jTtu1J$5957aef0e7310cbee88ea759a0b1df4054abb7e6d9545bf729454a0370783df36f5f15bdc3d2b639678c8dfdf442c1d3a9c7320a06e9ee124976d985ef1fa077'
    return check_password_hash(admin_password_hash, password)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if 'password' in request.form and check_admin_password(request.form['password']):
            session['logged_in'] = True
            return redirect(url_for('movie_form'))
        else:
            flash('Неверный пароль!')
    return render_template('admin.html')

@app.route('/movie_form', methods=['GET', 'POST'])
@app.route('/movie_form/<int:movie_id>', methods=['GET', 'POST'])  # Добавлен маршрут для редактирования
def movie_form(movie_id=None):
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    
    conn = get_db_connection()
    movie = None
    if movie_id:
        # Получаем фильм по ID для редактирования
        movie = conn.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()
    
    if request.method == 'POST':
        title = request.form['title']
        banner = request.form['banner']
        video_url = request.form['video_url']
        poster = request.form['poster']
        
        if movie:
            # Обновляем существующий фильм
            conn.execute('UPDATE movies SET title = ?, banner = ?, video_url = ?, poster = ? WHERE id = ?',
                         (title, banner, video_url, poster, movie_id))
        else:
            # Добавляем новый фильм
            conn.execute('INSERT INTO movies (title, banner, video_url, poster) VALUES (?, ?, ?, ?)',
                         (title, banner, video_url, poster))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('movie_form.html', movie=movie)

@app.route('/support')
def support():
    # Криптоадрес для копирования
    crypto_address = "TC2uMBYesp4tx16xxSeHzW2D9pEivFPRKr"
    return render_template('support.html', crypto_address=crypto_address)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
