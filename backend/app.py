import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from faq_generator import generate_faqs

def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route('/api/generate-faq', methods=['POST'])
    def handle_generate_faq():
        data = request.get_json()
        
        if not data or not data.get('content'):
            return jsonify({"success": False, "error": "Content is required"}), 400
            
        content = data.get('content')
        category = data.get('category', 'General')
        
        result = generate_faqs(content, category)
        
        if "error" in result:
            return jsonify({
                "success": False,
                "error": result["error"]
            }), 500
            
        return jsonify({
            "success": True,
            "faqs": result.get("faqs", [])
        })

    # Serve the frontend index at root
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    # Serve other static files
    @app.route('/<path:path>')
    def static_proxy(path):
        return send_from_directory(app.static_folder, path)
        
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)