import openai
import json
import re
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def build_prompt(resume_text, jd_text):
    return f"""
You are a recruitment assistant. Given the following job description and candidate resume, provide:

1) A matching score between 0 and 100 on how well the resume fits the job description.
2) A detailed explanation covering:
- Key skills matched/missing.
- Relevant experience (years, roles, domain).
- Compliance with mandatory criteria.
- Additional strengths/weaknesses.

Job Description:
{jd_text}

Resume:
{resume_text}

ONLY return a JSON object in this format:
{{
  "score": number from 0 to 100,
  "explanation": "detailed explanation here"
}}
Do not include anything else in the output.
"""

def get_match_score_and_explanation(resume_text, jd_text):
    prompt = build_prompt(resume_text, jd_text)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.3,
    )

    content = response.choices[0].message.content
    try:
        result = json.loads(content)
        score = result['score']
        explanation = result['explanation']
    except Exception:
        match = re.search(r"score\s*[:=]?\s*(\d{1,3})", content.lower())
        score = int(match.group(1)) if match else 0
        explanation = content  # Use full content if parsing fails
    return score, explanation

