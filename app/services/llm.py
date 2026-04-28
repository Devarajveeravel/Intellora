import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_llm_answer(query: str, context: str = ""):
    try:
        prompt = f"""
You are Intellora AI.

STRICT RULES:
- Always answer in bullet points
- No paragraphs
- Clean formatting
- If code → use proper markdown ``` blocks
- If context is given → answer ONLY from it
- If answer not found → say "• Not found in document"

Context:
{context}

Question:
{query}

Answer:
"""

        res = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        return res.choices[0].message.content.strip()

    except Exception as e:
        print("LLM ERROR:", e)
        return "• AI is not responding properly"