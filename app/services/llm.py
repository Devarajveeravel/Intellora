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
- ONLY bullet points
- NO paragraphs
- Each point in new line
- Use simple clear English
- Answer EXACTLY from context if available
- If context is empty → answer normally

Context:
{context}

User Question:
{query}

Answer format:
• point
• point
• point
"""

        res = client.chat.completions.create(
            model="llama3-70b-8192",  # ✅ STABLE + GOOD
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return res.choices[0].message.content

    except Exception as e:
        print("ERROR:", e)
        return "• AI is not responding properly right now"