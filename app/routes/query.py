from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm import generate_llm_answer

router = APIRouter()

memory = {}

class Query(BaseModel):
    query: str
    session_id: str
    file_text: str = ""


@router.post("/query")
def ask(q: Query):
    history = memory.get(q.session_id, "")

    # ✅ PRIORITY: PDF context first
    context = f"""
Previous conversation:
{history}

Document content:
{q.file_text}
"""

    answer = generate_llm_answer(q.query, context)

    # store memory (lightweight)
    memory[q.session_id] = history + f"\nUser: {q.query}\nAI: {answer}"

    return {"answer": answer}