# AI FAQ Generator (Week 1 scaffold)

This repo contains a lightweight scaffold for the "AI FAQ Generator" project. Week 1 focuses on learning and setting up the project environment.

Run locally (Python + Flask):

1. Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and set any keys

4. Run backend

```bash
python backend/app.py
```

5. Open the frontend at `frontend/index.html` in your browser or navigate to `http://localhost:5000/` if serving static files from Flask.

Notes:
- This scaffold provides a simple heuristic FAQ generator in `backend/utils.py`. In Week 3 we integrated an LLM API (OpenAI) and implemented prompt-based generation with a JSON output expectation. The backend will call OpenAI when `OPENAI_API_KEY` is set; otherwise it falls back to the local heuristic.
- The frontend is static and sends requests to `POST /api/generate`.

Environment example (`.env`):

```
PORT=5000
OPENAI_API_KEY= our_openai_api_key_here
```

Frontend controls:
- `Number of FAQs` — choose how many Q&A pairs to generate (1-20).
- `Copy All` — copy generated Q&A pairs to clipboard.
- `Export JSON` — download the generated FAQs as a JSON file.
