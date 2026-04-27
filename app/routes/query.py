from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm import generate_llm_answer
from app.services.rag import retrieve_context

router = APIRouter()

memory = {}

class Query(BaseModel):
    query: str
    session_id: str
    file_text: str = ""


@router.post("/query")
def ask(q: Query):
    history = memory.get(q.session_id, "")

    # 🔥 GET PDF CONTEXT
    rag_context = retrieve_context(q.query)

    # 🔥 FINAL CONTEXT
    context = history + "\n" + rag_context + "\n" + q.file_text

    answer = generate_llm_answer(q.query, context)

    memory[q.session_id] = history + f"\nUser: {q.query}\nAI: {answer}"

    return {"answer": answer}