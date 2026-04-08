import os
from flask import Flask
from storage.database import init_db
from api.routes import setup_routes

# Вказуємо шлях до папки static
template_dir = os.path.abspath('static')
app = Flask(__name__, static_folder=template_dir, static_url_path='')

init_db()
setup_routes(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)