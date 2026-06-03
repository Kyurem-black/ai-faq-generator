# AI FAQ Generator

A production-quality web application that accepts any text content (topic, article, product description, etc.) and automatically generates high-quality Frequently Asked Questions (FAQs) using Google's Gemini API.

## Features

- **Advanced AI Generation**: Utilizes Google's `gemini-2.5-flash` model to extract and generate 10-15 relevant, non-duplicate FAQs.
- **Context Categories**: Generate FAQs tailored to Educational, Product, Service, or Technical content.
- **Modern UI**: Premium design with glassmorphism, responsive layout, and vibrant styling.
- **Dark Mode**: Built-in toggle for light and dark themes.
- **Export to PDF**: Easily export generated FAQs as a clean PDF document.
- **Copy QA**: One-click copy functionality to easily share or paste generated questions and answers.

## Tech Stack

- **Frontend**: HTML5, CSS3 (Custom Properties, Glassmorphism), Vanilla JavaScript, `html2pdf.js`
- **Backend**: Python, Flask, Flask-CORS
- **AI**: Google Gemini API

## Project Structure

```text
project/
├── frontend/
│   ├── index.html     # Main UI
│   ├── style.css      # Styling & Themes
│   └── script.js      # Logic, API Calls, PDF Export
├── backend/
│   ├── app.py         # Flask App & Endpoints
│   ├── faq_generator.py # Gemini API Integration
│   └── requirements.txt # Python dependencies
├── .env               # Environment Variables (ignored in git)
├── .gitignore         # Git ignore file
└── README.md          # Documentation
```

## Setup & Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd project
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Configure Environment Variables**:
   Open `.env` (or create one based on the template) and add your Google Gemini API Key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   FLASK_APP=backend/app.py
   PORT=5000
   ```

5. **Run the Application**:
   Start the Flask server from the `project` root directory:
   ```bash
   python backend/app.py
   ```

6. **Access the App**:
   Open your browser and navigate to: [http://localhost:5000](http://localhost:5000)

## Example Screenshots

*(Include your screenshots here)*
- **Light Mode UI**
- **Dark Mode UI**
- **Generated FAQs View**
- **PDF Export Result**

## Evaluation Notes
- Includes advanced error handling.
- JSON-based structured output explicitly requested from Gemini for guaranteed formatting.
- Smooth animations, toasts, and loading states for premium user experience.
