import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# 🔥 FORMAT CLEAN LINE-BY-LINE (NO BULLETS)
def format_clean_lines(text: str):
    # Replace bullet symbols if model adds
    text = text.replace("•", "\n")

    # Split into lines
    lines = text.split("\n")

    clean = []
    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Capitalize first letter nicely
        line = line[0].upper() + line[1:] if len(line) > 1 else line

        clean.append(line)

    return "\n".join(clean)


def generate_llm_answer(query: str, context: str = ""):
    try:
        prompt = f"""
You are Intellora AI.

RULES:
- DO NOT use bullet symbols (•)
- DO NOT write paragraphs
- Write each point on a NEW LINE
- Each line should be clear and complete sentence
- Keep answers detailed but structured
- If code → use ``` blocks
- If context exists → answer ONLY from it
- If not found → say "Not found in document"

Context:
{context}

Question:
{query}
"""

        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        raw = res.choices[0].message.content.strip()

        # 🔥 CLEAN FORMAT
        return format_clean_lines(raw)

    except Exception as e:
        return f"Error: {str(e)}"