from flask import Blueprint, request, jsonify
from utils import generate_faqs

api_bp = Blueprint('api', __name__)


@api_bp.route('/generate', methods=['POST'])
def generate():
    data = request.get_json() or {}
    topic = (data.get('topic') or '').strip()
    content = (data.get('content') or '').strip()
    if not topic and not content:
        return jsonify({'error':'Provide topic or content'}), 400

    faqs = generate_faqs(topic=topic, content=content)
    return jsonify({'faqs': faqs})
