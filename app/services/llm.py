import os
import re
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# 🔥 FORCE CLEAN STRUCTURE (MAIN FIX)
def force_structure(text: str):
    text = text.replace("•", " ").replace("-", " ")
    text = re.sub(r"\s+", " ", text)

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    clean = []
    for s in sentences:
        s = s.strip()

        if not s:
            continue

        s = s[0].upper() + s[1:] if len(s) > 1 else s
        clean.append(s)

    return "\n".join(clean)


def generate_llm_answer(query: str, context: str = ""):
    try:
        prompt = f"""
You are Intellora AI.

STRICT RULES:
- Do NOT write paragraphs
- Do NOT use bullet points
- Each sentence must be separate line
- Keep answer detailed

Context:
{context}

Question:
{query}
"""

        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ WORKING MODEL
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        raw = res.choices[0].message.content.strip()

        # 🔥 HARD ENFORCE FORMAT
        return force_structure(raw)

    except Exception as e:
        return f"Error: {str(e)}"