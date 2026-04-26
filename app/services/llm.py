import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def format_response(text: str):
    if not text:
        return "No response"

    text = text.replace("\r", "\n")

    lines = text.split("\n")
    formatted = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # ❌ remove markdown junk
        line = line.replace("**", "")
        line = line.replace("*", "")  # REMOVE *
        line = line.replace("• •", "•")

        # Remove numbering
        line = re.sub(r"^\d+\.", "", line).strip()

        # 🔗 links
        if "http" in line:
            urls = re.findall(r'(https?://\S+)', line)
            for url in urls:
                formatted.append(f"\n🔗 {url}")
            continue

        # 🧠 HEADINGS
        if ":" in line and len(line.split()) < 6:
            formatted.append(f"\n{line}")
            continue

        # ✅ clean bullet
        if not line.startswith("•"):
            line = f"• {line}"

        formatted.append(line)

    return "\n".join(formatted)


def generate_llm_answer(query: str, context: str = ""):
    try:
        prompt = f"""
You are Intellora AI.

STRICT OUTPUT RULES (VERY IMPORTANT):
- DO NOT write paragraphs
- DO NOT use *
- DO NOT mix formats
- ONLY use:
    Heading:
    • point
    • point

- Leave space between sections
- Keep answers clean and readable
- Links should be separate

Context:
{context}

User Question:
{query}

Correct format example:

Definition:
• Point
• Point

Applications:
• Point
• Point

Now answer:
"""

        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        raw = res.choices[0].message.content
        return format_response(raw)

    except Exception as e:
        print("🔥 ERROR:", e)
        return "AI is not responding"