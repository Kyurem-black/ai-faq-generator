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
- This scaffold provides a simple heuristic FAQ generator in `backend/utils.py`. In Week 3 we'll integrate an LLM API (OpenAI or similar) and replace the heuristic with prompt-based generation.
- The frontend is static and sends requests to `POST /api/generate`.
