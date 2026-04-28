import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_llm_answer(query: str, context: str = ""):
    try:
        prompt = f"""
You are Intellora AI.

STRICT RULES:
- Always answer in bullet points
- No paragraphs
- Clean structure
- If code → use proper markdown ``` blocks
- If context is provided → answer ONLY from it
- If not found → say "• Not found in document"

Context:
{context}

Question:
{query}
"""

        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ FIXED MODEL
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        return res.choices[0].message.content.strip()

    except Exception as e:
        return f"• ERROR: {str(e)}"