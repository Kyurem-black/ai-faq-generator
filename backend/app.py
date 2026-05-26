from dotenv import load_dotenv
from flask import Flask, send_from_directory
from flask_cors import CORS
import os

load_dotenv()

def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    from routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    # Serve the frontend index at root
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    # Serve other static files (css, js)
    @app.route('/<path:path>')
    def static_proxy(path):
        return send_from_directory(app.static_folder, path)
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)