import subprocess
import time
import schedule

# Функция для выполнения действий в screen
def manage_screen_https():
    # Проверяем, существует ли сеанс screen с заданным именем
    check_session = subprocess.run(['screen', '-ls', 'anime-films-ssl'], capture_output=True, text=True)
    
    # Если сеанс существует, закрываем его
    if "anime-films-ssl" in check_session.stdout:
        subprocess.run(['screen', '-S', 'anime-films-ssl', '-X', 'quit'])
        time.sleep(3)  # Добавляем задержку после закрытия сеанса

    # Запускаем python приложение в новом сеансе screen
    subprocess.run(['screen', '-S', 'anime-films-ssl', '-d', '-m', 'python3', 'appssl.py'])

def manage_screen_http():
    # Проверяем, существует ли сеанс screen с заданным именем
    check_session = subprocess.run(['screen', '-ls', 'anime-films-http'], capture_output=True, text=True)
    
    # Если сеанс существует, закрываем его
    if "anime-films-http" in check_session.stdout:
        subprocess.run(['screen', '-S', 'anime-films-http', '-X', 'quit'])
        time.sleep(3)  # Добавляем задержку после закрытия сеанса

    # Запускаем python приложение в новом сеансе screen
    subprocess.run(['screen', '-S', 'anime-films-http', '-d', '-m', 'python3', 'app.py'])

# Запускаем функцию manage_screen_https() каждые 30 минут
schedule.every(30).minutes.do(manage_screen_https)

# Запускаем функцию manage_screen_http() каждые 90 минут
schedule.every(90).minutes.do(manage_screen_http)

# Запускаем бесконечный цикл для выполнения расписания
while True:
    schedule.run_pending()
    time.sleep(1)
