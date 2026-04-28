import os
from groq import Groq

# 🔥 INIT GROQ CLIENT
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# 🔥 FORCE BULLET FORMAT FUNCTION
def format_bullets(text: str):
    lines = text.strip().split("\n")

    clean = []
    for line in lines:
        line = line.strip()

        if not line:
            continue

        # ✅ Already bullet
        if line.startswith("•"):
            clean.append(line)

        # ✅ Numbered list → convert to bullet
        elif len(line) > 1 and line[0].isdigit():
            parts = line.split(".", 1)
            if len(parts) > 1:
                clean.append(f"• {parts[1].strip()}")
            else:
                clean.append(f"• {line}")

        # ✅ Normal sentence → force bullet
        else:
            clean.append(f"• {line}")

    return "\n".join(clean)


# 🔥 MAIN LLM FUNCTION
def generate_llm_answer(query: str, context: str = ""):
    try:
        prompt = f"""
You are Intellora AI.

STRICT RULES (MUST FOLLOW):
- ONLY bullet points
- EACH line MUST start with "•"
- NO paragraphs
- NO long text blocks
- Keep answers clean and structured
- If code → use proper ```code blocks```
- If context exists → answer ONLY from it
- If answer not found in context → say "• Not found in document"

Context:
{context}

Question:
{query}

Answer:
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        raw_output = response.choices[0].message.content.strip()

        # 🔥 FORCE STRUCTURED BULLETS
        final_output = format_bullets(raw_output)

        return final_output

    except Exception as e:
        return f"• ERROR: {str(e)}"