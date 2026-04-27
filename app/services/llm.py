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
- Always answer in bullet points
- No paragraphs
- Use clear structured format
- If document is provided → answer ONLY from document
- If not found → say "Not found in document"

Context:
{context}

User Question:
{query}

Answer format:
• point
• point
"""

        res = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        return res.choices[0].message.content

    except Exception as e:
        print("LLM ERROR:", e)
        return "• AI is not responding properly right now"