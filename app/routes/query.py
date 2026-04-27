from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm import generate_llm_answer

router = APIRouter()

memory = {}

class Query(BaseModel):
    query: str
    session_id: str
    file_text: str = ""


def get_relevant_context(file_text, query):
    if not file_text:
        return ""

    chunks = file_text.split("\n")

    # simple keyword match (FAST + WORKS)
    relevant = []
    for chunk in chunks:
        if any(word.lower() in chunk.lower() for word in query.split()):
            relevant.append(chunk)

    return "\n".join(relevant[:20])  # limit


@router.post("/query")
def ask(q: Query):
    history = memory.get(q.session_id, "")

    file_context = get_relevant_context(q.file_text, q.query)

    context = f"""
Chat History:
{history}

Document Context:
{file_context}
"""

    answer = generate_llm_answer(q.query, context)

    memory[q.session_id] = history + f"\nUser: {q.query}\nAI: {answer}"

    return {"answer": answer}