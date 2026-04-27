import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# 🔥 CLEAN FORMATTER
def format_response(text: str):
    lines = text.split("\n")
    formatted = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # remove markdown noise
        line = re.sub(r"[*_`#>-]", "", line).strip()

        # remove numbering
        line = re.sub(r"^\d+[\).\s-]*", "", line)

        # links
        if "http" in line:
            urls = re.findall(r'(https?://\S+)', line)
            for url in urls:
                formatted.append(f"🔗 {url}")
        else:
            # force bullet
            formatted.append(f"• {line}")

    return "\n".join(formatted)


# 🔥 MAIN LLM
def generate_llm_answer(query: str, context: str = ""):
    try:
        prompt = f"""
You are Intellora AI — a high-quality assistant like ChatGPT.

STRICT RULES (VERY IMPORTANT):
- ALWAYS answer in bullet points
- NO paragraphs
- Each bullet = ONE clear idea
- Use simple clear English
- Give correct definitions (no guessing)
- If coding → give proper code blocks
- If PDF context exists → answer ONLY from it
- If no context → answer normally with knowledge

FORMAT:
• Point 1
• Point 2
• Point 3

---------------------

Context:
{context[:4000]}

---------------------

User Question:
{query}

Answer:
"""

        res = client.chat.completions.create(
    model="mixtral-8x7b-32768",  # ✅ SAFE MODEL
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3
     )

        raw = res.choices[0].message.content

        return format_response(raw)

    except Exception as e:
        print("LLM ERROR:", e)
        return "• AI is not responding properly right now"