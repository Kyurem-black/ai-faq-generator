import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_faqs(content, category="General"):
    system_prompt = f"""You are a professional documentation specialist and customer support expert.

Analyze the provided content and generate Frequently Asked Questions for the category: {category}.

Requirements:
- Generate realistic user questions.
- Cover beginner and advanced concepts.
- Include troubleshooting questions when relevant.
- Avoid duplicate questions.
- Answers should be clear and concise.
- Use professional language.
- Generate 10-15 FAQs.

Return ONLY valid JSON.

Format:
{{
  "faqs": [
    {{
      "question": "...",
      "answer": "..."
    }}
  ]
}}
"""
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Content to analyze:\n\n{content}",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                temperature=0.7,
            ),
        )
        
        result_content = response.text
        return json.loads(result_content)
    except Exception as e:
        print(f"Error generating FAQs: {e}")
        return {"faqs": [], "error": str(e)}
