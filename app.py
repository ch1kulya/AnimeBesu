from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
from werkzeug.security import check_password_hash
import sqlite3
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание обработчика для записи логов в файл
file_handler = logging.FileHandler('besu.log')
file_handler.setLevel(logging.INFO)

# Создание обработчика для вывода логов на консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Создание форматтера для логов
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Добавление обработчиков к логгеру приложения
logger.addHandler(file_handler)
logger.addHandler(console_handler)

app = Flask(__name__)
app.secret_key = 'SECRET_KEY' # Для разработки

# Функция для инициализации базы данных
def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS movies (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        banner TEXT,
                        video_url TEXT,
                        poster TEXT,
                        description TEXT,
                        views INTEGER DEFAULT 0
                        )''')
    conn.close()
    logger.info("Database initialized successfully.")

# Функция для получения соединения с базой данных
def get_db_connection():
    conn = sqlite3.connect('besu.db')
    conn.row_factory = sqlite3.Row
    return conn

# Проверка и инициализация базы данных при запуске приложения
init_db()

# Функция для получения топ-15 самых просматриваемых фильмов
def get_top_movies():
    conn = get_db_connection()
    top_movies = conn.execute('SELECT * FROM movies ORDER BY views DESC LIMIT 15').fetchall()
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
    logger.info(f'Views increased for movie ID {movie_id}.')
    movie = conn.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()
    conn.close()
    if movie is not None:
        return render_template('watch.html', title=f'{movie["title"]} | Anime Besu', meta_description=f'Watch {movie["title"]} anime movie online for free.', movie=movie)
    else:
        return redirect(url_for('index'))

# Функция для проверки пароля
def check_admin_password(password):
    admin_password_hash = 'scrypt:32768:8:1$XB7ZdR7608jTtu1J$5957aef0e7310cbee88ea759a0b1df4054abb7e6d9545bf729454a0370783df36f5f15bdc3d2b639678c8dfdf442c1d3a9c7320a06e9ee124976d985ef1fa077'
    return check_password_hash(admin_password_hash, password)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if 'password' in request.form and check_admin_password(request.form['password']):
            session['logged_in'] = True
            logger.info('Admin logged in successfully.')
            return redirect(url_for('movie_form'))
        else:
            flash('Incorrect password!')
            logger.warning('Failed login attempt.')
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
        logger.info('Movie added/updated successfully.')
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('movie_form.html', title='Anime Besu Form', meta_description='Anime Besu Form.', movie=movie, top_movies=top_movies)

@app.route('/logs')
def view_logs():
    if not session.get('logged_in'):
        return redirect(url_for('admin'))

    # Чтение содержимого файла логов
    with open('app.log', 'r') as log_file:
        logs = log_file.read()

    return Response(logs, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969, debug=False)
