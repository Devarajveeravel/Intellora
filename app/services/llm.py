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
- Give clean bullet points
- No long paragraphs
- Use markdown (**bold**, code blocks if needed)
- If from document → answer ONLY from context
- If not found → say "Not found in document"

Context:
{context}

User Question:
{query}

Answer:
"""

        res = client.chat.completions.create(
            model="llama3-70b-8192",  # stable + best
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        return res.choices[0].message.content.strip()

    except Exception as e:
        print("LLM ERROR:", e)
        return "❌ AI is not responding properly right now"