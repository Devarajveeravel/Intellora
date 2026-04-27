import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_llm_answer(query: str, context: str = ""):
    try:
        prompt = f"""
You are Intellora AI.

RULES:
- Answer ONLY from given context if available
- If PDF content exists → prioritize it STRICTLY
- NO fake answers
- Format cleanly using bullet points
- Use short, sharp points
- Use headings if needed
- No long paragraphs

CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER FORMAT:
• Point
• Point
• Point
"""

        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ stable + fast
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return res.choices[0].message.content

    except Exception as e:
        print("ERROR:", e)
        return "❌ AI is not responding properly right now"