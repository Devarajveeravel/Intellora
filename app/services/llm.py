import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# 🔥 FORMAT CLEANER
def format_response(text: str):
    lines = text.split("\n")
    formatted = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # remove markdown symbols
        line = re.sub(r"[*_`#>-]", "", line)

        # remove numbering
        line = re.sub(r"^\d+[\).\s-]*", "", line)

        # links
        if "http" in line:
            urls = re.findall(r'(https?://\S+)', line)
            for url in urls:
                formatted.append(f"🔗 {url}")
        else:
            formatted.append(f"• {line}")

    return "\n".join(formatted)


# 🔥 MAIN FUNCTION
def generate_llm_answer(query: str, context: str = ""):
    try:
        prompt = f"""
You are Intellora AI.

STRICT RULES:
- Always give correct answers
- Never guess wrong meanings
- Always respond in bullet points
- No paragraphs
- Each bullet = one clear idea
- Keep it simple and accurate
- If context exists → use it
- If no context → use your knowledge

FORMAT:
• Point
• Point
• Point

------------------
Context:
{context[:3000]}
------------------

Question:
{query}

Answer:
"""

        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # ✅ STABLE MODEL
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        raw = res.choices[0].message.content

        return format_response(raw)

    except Exception as e:
        print("LLM ERROR:", e)
        return "• AI is temporarily unavailable. Try again."