import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def format_response(text: str):
    lines = text.split("\n")
    formatted = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Remove markdown
        line = line.replace("**", "").replace("•", "").strip()

        # Convert numbered list to bullet
        line = re.sub(r"^\d+\.", "", line).strip()

        # Detect links
        if "http" in line:
            urls = re.findall(r'(https?://\S+)', line)
            for url in urls:
                formatted.append(f"🔗 {url}")
        else:
            formatted.append(f"• {line}")

    return "\n".join(formatted)


def generate_llm_answer(query: str, context: str = ""):
    try:
        prompt = f"""
You are Intellora AI (premium assistant).

STRICT RULES:
- NO paragraphs
- ONLY bullet points
- Short, clean, structured answers
- If useful → include links

Context:
{context}

User Question:
{query}

Answer format:
• Point
• Point

"""

        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )

        raw = res.choices[0].message.content
        return format_response(raw)

    except Exception as e:
        print("ERROR:", e)
        return "AI is not responding"