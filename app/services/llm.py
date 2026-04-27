import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_llm_answer(query: str, context: str = ""):
    try:
        prompt = f"""
You are Intellora AI — a highly intelligent assistant like ChatGPT.

RULES:
- Give CLEAR, HIGH-QUALITY answers
- Use bullet points ONLY when useful
- Use paragraphs for explanation when needed
- Answer like a human expert (NOT robotic)
- If context is provided → use it STRICTLY

CONTEXT (from uploaded file):
{context[:3000]}

USER QUESTION:
{query}

RESPONSE STYLE:
- Start with a clear answer
- Then explain
- Then give bullets if needed
- NO fake or generic answers
"""

        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # ✅ Stable + fast
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )

        return res.choices[0].message.content.strip()

    except Exception as e:
        print("ERROR:", e)
        return "❌ AI is not responding properly right now"