import re

def _split_sentences(text):
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p.strip() for p in parts if p.strip()]

def generate_faqs(topic='', content=''):
    """Very small heuristic generator for Week 1.
    If `content` provided, pick up to 4 sentences and convert to QA pairs.
    If only `topic` provided, return generic FAQs for the topic.
    """
    faqs = []
    if content:
        sents = _split_sentences(content)
        for s in sents[:4]:
            words = s.split()
            subject = ' '.join(words[:6]) if words else topic or 'this topic'
            q = f'What is {subject.strip(".,")} ?'
            faqs.append({'question': q, 'answer': s})
    else:
        # generic FAQs for a topic
        faqs = [
            {'question': f'What is {topic}?', 'answer': f'{topic} refers to ... (add details).'},
            {'question': f'How does {topic} work?', 'answer': 'Explain core workflow, steps and actors.'},
            {'question': f'Common issues with {topic}?', 'answer': 'List common issues and troubleshooting steps.'}
        ]
    return faqs
