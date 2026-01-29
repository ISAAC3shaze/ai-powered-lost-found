import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def explain_match(lost_desc, found_desc, location_hint=None):
    prompt = f"""
You are an AI assistant explaining why a lost item matches a found item.

Lost item description:
"{lost_desc}"

Found item description:
"{found_desc}"

Location context:
"{location_hint if location_hint else 'Not provided'}"

Explain the match in one clear sentence for a student user.
Do not mention AI models or embeddings.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return None
