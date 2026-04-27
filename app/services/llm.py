import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ✅ FORMAT RESPONSE
def format_response(text: str):
    lines = text.split("\n")
    formatted = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # remove markdown symbols
        line = line.replace("**", "").replace("*", "").strip()

        # remove numbering
        line = re.sub(r"^\d+\.", "", line).strip()

        # detect links
        if "http" in line:
            urls = re.findall(r"(https?://\S+)", line)
            for url in urls:
                formatted.append(f"🔗 {url}")
        else:
            formatted.append(f"• {line}")

    return "\n".join(formatted)


# ✅ MAIN FUNCTION
def generate_llm_answer(query: str, context: str = ""):
    try:
        # limit context
        if context:
            context = context[:6000]

        prompt = f"""
Answer the question clearly.

RULES:
- ONLY bullet points
- NO paragraphs
- NO introductions like "I am Intellora"
- Keep answers short and useful
- If context is provided → answer ONLY from context

Context:
{context}

Question:
{query}

Answer:
• point
• point
"""

        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        raw = res.choices[0].message.content

        return format_response(raw)

    except Exception as e:
        print("LLM ERROR:", e)
        return "❌ AI not responding properly"