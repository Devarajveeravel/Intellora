import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_llm_answer(query: str, context: str = ""):
    try:
        prompt = f"""
You are Intellora AI.

- Answer ONLY in bullet points
- No paragraphs
- Use clean structure
- If code → use markdown ``` blocks
- If context given → answer from it

Context:
{context}

Question:
{query}
"""

        res = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
        )

        return res.choices[0].message.content.strip()

    except Exception as e:
        return f"• ERROR: {str(e)}"