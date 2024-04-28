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

# Функция для получения топ-10 самых просматриваемых фильмов
def get_top_movies():
    conn = get_db_connection()
    top_movies = conn.execute('SELECT * FROM movies ORDER BY views DESC LIMIT 10').fetchall()
    conn.close()
    return top_movies

@app.route('/')
def index():
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM movies ORDER BY views DESC').fetchall()
    conn.close()
    return render_template('index.html', title='Anime Besu', meta_description='Watch anime movies online for free.', movies=movies)

@app.route('/watch/<int:movie_id>')
def watch(movie_id):
    conn = get_db_connection()
    conn.execute('UPDATE movies SET views = views + 1 WHERE id = ?', (movie_id,))
    conn.commit()
    movie = conn.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()
    conn.close()
    if movie is not None:
        return render_template('watch.html', title=f'{movie["title"]} | Anime Besu', meta_description=f'Watch {movie["title"]} anime movie online for free.', movie=movie)
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
            flash('Incorrect password!')
    return render_template('admin.html', title='Anime Besu Admin', meta_description='Anime Besu Admin Panel.')

@app.route('/movie_form', methods=['GET', 'POST'])
@app.route('/movie_form/<int:movie_id>', methods=['GET', 'POST'])
def movie_form(movie_id=None):
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    
    top_movies = get_top_movies()  # Получаем топ-10 фильмов
    
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
        description = request.form['description']  # Получаем описание из формы

        if movie:
            # Обновляем существующий фильм
            conn.execute('UPDATE movies SET title = ?, banner = ?, video_url = ?, poster = ?, description = ? WHERE id = ?',
                         (title, banner, video_url, poster, description, movie_id))
        else:
            # Добавляем новый фильм
            conn.execute('INSERT INTO movies (title, banner, video_url, poster, description) VALUES (?, ?, ?, ?, ?)',
                         (title, banner, video_url, poster, description))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('movie_form.html', title='Anime Besu Form', meta_description='Anime Besu Form.', movie=movie, top_movies=top_movies)

@app.route('/support')
def support():
    # Криптоадрес для копирования
    crypto_address = "TC2uMBYesp4tx16xxSeHzW2D9pEivFPRKr"
    return render_template('support.html', title='Anime Besu Support', meta_description='Anime Besu Support.', crypto_address=crypto_address)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, debug=False, ssl_context=('/etc/letsencrypt/live/ch1ka.su/fullchain.pem', '/etc/letsencrypt/live/ch1ka.su/privkey.pem'))
