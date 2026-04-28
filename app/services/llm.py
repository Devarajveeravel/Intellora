import os
import re
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# 🔥 FORCE STRUCTURE (REAL FIX)
def force_structure(text: str):
    # Remove bullet symbols
    text = text.replace("•", " ").replace("-", " ")

    # Normalize spaces
    text = re.sub(r"\s+", " ", text)

    # Split into sentences (very important)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    clean = []
    for s in sentences:
        s = s.strip()

        if not s:
            continue

        # Capitalize properly
        s = s[0].upper() + s[1:] if len(s) > 1 else s

        clean.append(s)

    return "\n".join(clean)


def generate_llm_answer(query: str, context: str = ""):
    try:
        prompt = f"""
You are Intellora AI.

STRICT RULES:
- Do NOT write paragraphs
- Do NOT use bullet symbols
- Write clear full sentences
- Each idea must be a separate sentence

Context:
{context}

Question:
{query}
"""

        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        raw = res.choices[0].message.content.strip()

        # 🔥 HARD FIX HERE
        return force_structure(raw)

    except Exception as e:
        return f"Error: {str(e)}"