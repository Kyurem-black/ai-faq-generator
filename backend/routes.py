from flask import Blueprint, request, jsonify
from utils import generate_faqs

api_bp = Blueprint('api', __name__)


@api_bp.route('/generate', methods=['POST'])
def generate():
    data = request.get_json() or {}
    topic = (data.get('topic') or '').strip()
    content = (data.get('content') or '').strip()
    try:
        num = int(data.get('num', 5))
    except Exception:
        num = 5

    if not topic and not content:
        return jsonify({'error': 'Provide topic or content'}), 400

    try:
        faqs = generate_faqs(topic=topic, content=content, num=num)
        return jsonify({'faqs': faqs})
    except Exception as e:
        # Log error server-side and return a clean message to client
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error generating FAQs.'}), 500


@api_bp.route('/debug_sample', methods=['GET'])
def debug_sample():
    sample = "Anime refers to hand-drawn or computer-generated animation originating from Japan. Globally, the term specifically describes Japanese animation, characterized by colorful artwork, expressive and exaggerated characters, and diverse themes suitable for all ages."
    faqs = generate_faqs(topic='Anime', content=sample, num=5)
    return jsonify({'faqs': faqs})
