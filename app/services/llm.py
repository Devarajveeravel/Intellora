import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_llm_answer(query: str, context: str = ""):
    try:
        prompt = f"""
You are an intelligent AI assistant.

STRICT RULES:
- Answer ONLY from the provided context if available
- If context is empty, answer normally
- ALWAYS use bullet points
- NO paragraphs
- NO long explanations
- Keep answers short and clean
- If you don't know → say "Not found in document"

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
            model="llama-3.1-8b-instant",  # ✅ stable
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        return res.choices[0].message.content.strip()

    except Exception as e:
        print("LLM ERROR:", e)
        return "AI is not responding properly right now"