import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def format_response(text: str):
    """
    Clean and structure AI output nicely
    """

    if not text:
        return "No response"

    # Normalize spacing
    text = text.replace("\r", "\n")

    # Split lines
    lines = text.split("\n")
    formatted = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Remove markdown artifacts
        line = line.replace("**", "").strip()

        # Convert numbered lists → bullets
        line = re.sub(r"^\d+\.", "•", line)

        # Detect links
        urls = re.findall(r'(https?://\S+)', line)
        if urls:
            for url in urls:
                formatted.append(f"🔗 {url}")
            continue

        # Keep headings clean (no bullet)
        if line.endswith(":"):
            formatted.append(line)
            continue

        # Add bullet if not already
        if not line.startswith("•"):
            line = f"• {line}"

        formatted.append(line)

    return "\n".join(formatted)


def generate_llm_answer(query: str, context: str = ""):
    try:
        prompt = f"""
You are Intellora AI (a smart and clean assistant).

RULES:
- Give clear, structured answers
- Use bullet points for key info
- Use headings when needed (like "Definition:", "Applications:")
- Avoid long paragraphs
- Keep answers readable and professional
- If useful, include links (each on a new line)

Context:
{context}

User Question:
{query}

Answer cleanly:
"""

        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )

        raw = res.choices[0].message.content
        return format_response(raw)

    except Exception as e:
        print("🔥 ERROR:", e)
        return "AI is not responding"