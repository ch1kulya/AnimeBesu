### Anime Besu

Anime Besu is a Flask-based web application that allows users to watch anime movies online for free. This README.md file provides an overview of the application's functionality, setup instructions, and additional details for developers.

#### Features:

- **Watch Anime Movies**: Users can watch anime movies directly on the platform.
- **Admin Panel**: Secure admin panel for managing movies, accessed with a password.
- **Logging**: Logs admin login attempts and movie views.
- **Support Page**: Provides a crypto address for donations.
- **Scheduled Restarts**: Automatically restarts the HTTP and HTTPS versions of the application periodically.

#### Prerequisites:

- Python 3.x
- Flask
- SQLite3
- Werkzeug

#### Installation and Setup:

1. Clone the repository: `git clone <repository_url>`
2. Navigate to the project directory: `cd <project_directory>`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application:
   - For HTTP version: `python app.py`
   - For HTTPS version: `python appssl.py`
5. Access the application in your web browser: `http://localhost` for HTTP or `https://localhost` for HTTPS.

#### File Structure:

- **app.py**: Main Flask application for serving HTTP requests.
- **appssl.py**: Similar to app.py but configured for HTTPS.
- **restart.py**: Python script for managing automatic restarts of the application.
- **templates/**: Contains HTML templates for different pages.
- **static/**: Static assets like CSS, images, and JavaScript.

#### Usage:

- Access the main page to browse and watch anime movies.
- Access the admin panel (`/admin`) to manage movies. Use the provided password for authentication.
- Access the support page (`/support`) to find the crypto address for donations.
- Access the logs page (`/logs`) to view application logs (requires admin authentication).

#### Logging:

- Application logs are stored in `app.log`.
- Log entries include timestamps, log levels, and messages.

#### Scheduled Restarts:

- The `restart.py` script manages automatic restarts of both HTTP and HTTPS versions of the application.
- HTTP version restarts every 90 minutes, and HTTPS version restarts every 30 minutes.

#### Security:

- The admin panel is protected with a password hash stored in the code.
- HTTPS version is secured with SSL/TLS certificates.

#### Contributors:

- **Maintainer**: [ch1kulya](https://github.com/ch1kulya)

Enjoy watching anime movies on Anime Besu! 🎬🍿
