import subprocess
import time
import schedule
import logging

HttpsApp = 'anime-films-ssl'
HttpApp = 'anime-films-http'

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание обработчика для записи логов в файл
file_handler = logging.FileHandler('app.log')
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

# Функция для выполнения действий в screen
def manage_screen_https():
    # Проверяем, существует ли сеанс screen с заданным именем
    check_session = subprocess.run(['screen', '-ls', HttpsApp], capture_output=True, text=True)
    
    # Если сеанс существует, закрываем его
    if "anime-films-ssl" in check_session.stdout:
        subprocess.run(['screen', '-S', HttpsApp, '-X', 'quit'])
        time.sleep(3)  # Добавляем задержку после закрытия сеанса

    # Запускаем python приложение в новом сеансе screen
    subprocess.run(['screen', '-S', HttpsApp, '-d', '-m', 'python3', 'appssl.py'])

    logger.info(f'Application {HttpsApp} restarted successfully.')

def manage_screen_http():
    # Проверяем, существует ли сеанс screen с заданным именем
    check_session = subprocess.run(['screen', '-ls', HttpApp], capture_output=True, text=True)
    
    # Если сеанс существует, закрываем его
    if "anime-films-http" in check_session.stdout:
        subprocess.run(['screen', '-S', HttpApp, '-X', 'quit'])
        time.sleep(3)  # Добавляем задержку после закрытия сеанса

    # Запускаем python приложение в новом сеансе screen
    subprocess.run(['screen', '-S', HttpApp, '-d', '-m', 'python3', 'app.py'])

    logger.info(f'Application {HttpApp} restarted successfully.')

# Запускаем функцию manage_screen_https() каждые 30 минут
schedule.every(30).minutes.do(manage_screen_https)

# Запускаем функцию manage_screen_http() каждые 90 минут
schedule.every(90).minutes.do(manage_screen_http)

# Запускаем бесконечный цикл для выполнения расписания
while True:
    schedule.run_pending()
    time.sleep(1)
