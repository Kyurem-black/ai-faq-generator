from dotenv import load_dotenv
from flask import Flask
import os

load_dotenv()

def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    from routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)