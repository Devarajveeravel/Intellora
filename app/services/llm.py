import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# 🔥 STRONG BULLET FORMATTER (FIXES YOUR ISSUE)
def format_bullets(text: str):
    # Split using bullet symbol
    parts = text.split("•")

    clean = []
    for part in parts:
        part = part.strip()

        if not part:
            continue

        clean.append(f"• {part}")

    return "\n".join(clean)


def generate_llm_answer(query: str, context: str = ""):
    try:
        prompt = f"""
You are Intellora AI.

STRICT RULES:
- ONLY bullet points
- Each point MUST start with "•"
- NO paragraphs
- Keep answers short and structured
- If code → use ``` blocks
- If context exists → answer ONLY from it
- If not found → say "• Not found in document"

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

        # 🔥 FORCE PROPER LINE-BY-LINE BULLETS
        return format_bullets(raw)

    except Exception as e:
        return f"• ERROR: {str(e)}"