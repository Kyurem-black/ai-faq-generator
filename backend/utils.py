import os
import re
import difflib
import json

try:
    import openai
except Exception:
    openai = None

OPENAI_KEY = (os.environ.get('OPENAI_API_KEY') or '').strip()
if openai and OPENAI_KEY:
    openai.api_key = OPENAI_KEY


def _split_sentences(text):
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p.strip() for p in parts if p.strip()]


def _extract_json(text):
    # Attempt to find the first JSON array or object in the model output
    m = re.search(r'(\{[\s\S]*\}|\[[\s\S]*\])', text)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def _dedupe_faqs(faqs, q_threshold=0.78, a_threshold=0.85):
    """Remove near-duplicate FAQs using simple string similarity on questions and answers."""
    unique = []
    for f in faqs:
        q = re.sub(r"\s+", " ", (f.get('question') or '').strip().lower())
        a = re.sub(r"\s+", " ", (f.get('answer') or '').strip().lower())
        is_dup = False
        for u in unique:
            uq = re.sub(r"\s+", " ", (u.get('question') or '').strip().lower())
            ua = re.sub(r"\s+", " ", (u.get('answer') or '').strip().lower())
            qsim = difflib.SequenceMatcher(None, q, uq).ratio()
            asim = difflib.SequenceMatcher(None, a, ua).ratio()
            if qsim >= q_threshold or asim >= a_threshold:
                is_dup = True
                break
        if not is_dup:
            unique.append(f)
    return unique


def _llm_generate(topic, content, num=5, model=None):
    if not openai or not OPENAI_KEY:
        return None

    # Prefer an advanced model by default (overridable via OPENAI_MODEL env var)
    model = model or os.environ.get('OPENAI_MODEL') or 'gpt-4.1-mini'

    # Stronger prompt with explicit constraints and an example. We also retry the LLM call a few times
    system_msg = (
        "You are a professional FAQ generation expert.\n"
        "Produce human-like FAQs: natural, concise, and useful.\n"
        "- Do NOT copy sentences verbatim from the content; synthesize clear questions.\n"
        "- Questions should begin with an interrogative word (What/How/Why/When/Who/Where) and be concise (<=12 words).\n"
        "- Answers should be 1-2 short sentences (prefer <=30 words).\n"
        "- Return JSON only: an array of objects with keys `question` and `answer`.\n"
        "Example output (5 items):\n"
        "[\n  {\"question\": \"What is Anime?\", \"answer\": \"Japanese-origin animation characterized by colorful artwork and diverse themes.\"},\n  {\"question\": \"Who typically creates anime?\", \"answer\": \"Studios and independent artists in Japan, using hand-drawn or digital techniques.\"}\n]"
    )

    user_msg = (
        f"Generate {num} FAQs from the information below.\n\n"
        f"Topic:\n{topic}\n\n"
        f"Content:\n{content}\n\n"
        "Return JSON only, no surrounding markdown or commentary. Follow constraints in system message."
    )

    text = None
    for attempt in range(3):
        try:
            resp = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.12,
                max_tokens=900,
            )
            text = resp['choices'][0]['message']['content']
            if text:
                break
        except Exception:
            # small backoff
            import time
            time.sleep(0.6 * (attempt + 1))
            text = None

    # After attempts, if we never received text, give up
    if not text:
        return None

    # Strip code fences if present
    if text.strip().startswith('```'):
        parts = text.split('\n')
        if parts[0].startswith('```'):
            parts = parts[1:]
        if parts and parts[-1].startswith('```'):
            parts = parts[:-1]
        text = '\n'.join(parts)

    # parse robustly
    try:
        parsed = json.loads(text)
    except Exception:
        parsed = _extract_json(text)

    out = []
    if isinstance(parsed, list):
        for item in parsed[:num]:
            if not isinstance(item, dict):
                continue
            q = item.get('question') or item.get('q') or item.get('question_text')
            a = item.get('answer') or item.get('a') or item.get('answer_text')
            if q and a:
                out.append({'question': q.strip(), 'answer': a.strip()})

    # If we have initial content, run a single refinement pass to clean phrasing
        if out:
            refined = _refine_faqs_with_llm(out, num=num, model=model)
        if refined:
            return refined
        return out

    return None


def _refine_faqs_with_llm(faqs, num=None, model=None):
    """Send the generated FAQ list back to the LLM and ask for a single-pass refinement
    to ensure natural-sounding questions and concise answers. Returns refined list or None."""
    if not openai or not OPENAI_KEY:
        return None
    model = model or os.environ.get('OPENAI_MODEL') or 'gpt-4.1-mini'

    # Prepare JSON payload as compact string
    try:
        payload = json.dumps(faqs, ensure_ascii=False)
    except Exception:
        return None

    system = (
        "You are an expert copy editor for FAQs.\n"
        "Refine each FAQ so questions are natural, start with an interrogative word, and are concise (<=12 words).\n"
        "Make answers 1-2 short sentences (<=30 words). Preserve meaning. Return JSON only with the same structure.\n"
        "Example input and output:\nInput: [{\"question\":\"What is X\",\"answer\":\"Long text...\"}]\nOutput: [{\"question\":\"What is X?\",\"answer\":\"Short concise answer.\"}]"
    )

    user = (
        "Refine the following JSON array of FAQ objects. Return JSON only. Do not add extra fields.\n"
        "Ensure questions are diverse and do not repeat the same phrasing; prefer different interrogatives across items.\n"
        f"Return exactly {num if num else 'the same number of'} items if possible.\n\n"
        f"Input: {payload}"
    )

    text = None
    for attempt in range(3):
        try:
            resp = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=0.7,
                max_tokens=800,
            )
            text = resp['choices'][0]['message']['content']
            if text:
                break
        except Exception:
            import time
            time.sleep(0.5 * (attempt + 1))
            text = None

    if not text:
        return None

    # strip fences
    if text.strip().startswith('```'):
        parts = text.split('\n')
        if parts[0].startswith('```'):
            parts = parts[1:]
        if parts and parts[-1].startswith('```'):
            parts = parts[:-1]
        text = '\n'.join(parts)

    try:
        parsed = json.loads(text)
    except Exception:
        parsed = _extract_json(text)

    if isinstance(parsed, list):
        out = []
        for item in parsed:
            if not isinstance(item, dict):
                continue
            q = item.get('question') or item.get('q')
            a = item.get('answer') or item.get('a')
            if q and a:
                out.append({'question': q.strip(), 'answer': a.strip()})
        if out:
            return out

    return None


def generate_faqs(topic='', content='', num=5):
    """Generate FAQs. Tries LLM (OpenAI) when API key is set; falls back to heuristic.

    Returns a list of {question, answer} dicts.
    """
    print('generate_faqs called: topic=', topic, 'num=', num)
    # Attempt LLM generation
    faqs = _llm_generate(topic, content, num=num)
    if faqs:
        # If LLM returned enough diverse items, use it. Otherwise produce deterministic diverse list.
        faqs = _dedupe_faqs(faqs)
        if len(faqs) >= num:
            return faqs[:num]
        # Otherwise ignore the sparse LLM output and produce deterministic fill
        def _heuristic_fill(topic, content, needed):
            out = []
            templates = [
                'What is {s}?',
                'How is {s} created?',
                'Why is {s} important?',
                'Who typically produces {s}?',
                'When did {s} originate?'
            ]
            sents = _split_sentences(content) if content else []
            for sentence in sents:
                if len(out) >= needed:
                    break
                m = re.match(r'^(?P<sub>[^\.\,\n]+?)\s+(is|are|refers to)\s+', sentence, flags=re.I)
                if m:
                    subj = m.group('sub').strip()
                else:
                    subj = topic or 'this topic'
                for t in templates:
                    if len(out) >= needed:
                        break
                    q = t.format(s=subj)
                    a = sentence if len(sentence.split()) <= 30 else ' '.join(sentence.split()[:30]) + '...'
                    out.append({'question': q, 'answer': a})
            i = 0
            while len(out) < needed:
                s = topic or 'this topic'
                q = templates[i % len(templates)].format(s=s)
                out.append({'question': q, 'answer': f'{s} - brief overview.'})
                i += 1
            return out

        faqs = _dedupe_faqs(_heuristic_fill(topic, content, num * 2))[:num]
        return faqs

    # Fallback heuristic
    faqs = []
    if content:
        sents = _split_sentences(content)
        for s in sents[:max(1, min(4, num))]:
            # try to generate a more natural question via simple heuristics
            # if sentence contains ' is ' or ' are ', use 'What is/are X?'
            m = re.match(r'^(?P<sub>[^\.\,\n]+?)\s+(is|are|refers to)\s+(?P<rest>.+)$', s, flags=re.I)
            if m:
                subject = m.group('sub').strip()
                q = f'What is {subject}?'
            else:
                # fallback generic phrasing
                q = f'What should I know about {subject if (subject:=topic) else "this"}?'
                faqs.append({'question': q, 'answer': s})
            faqs = _dedupe_faqs(faqs)
    else:
        # generic templates when only topic is available
        templates = [
            (f'What is {topic}?', f'{topic} refers to ... (add details).'),
            (f'How does {topic} work?', 'Explain core workflow, steps and actors.'),
            (f'What are common issues with {topic}?', 'List common issues and troubleshooting steps.'),
        ]
        for t in templates[:num]:
            faqs.append({'question': t[0], 'answer': t[1]})

    return faqs
