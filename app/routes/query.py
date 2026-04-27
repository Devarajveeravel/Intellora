from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm import generate_llm_answer
from app.routes.upload import uploaded_data  # ✅ IMPORTANT

router = APIRouter()

memory = {}

class Query(BaseModel):
    query: str
    session_id: str


@router.post("/query")
def ask(q: Query):
    history = memory.get(q.session_id, "")

    # ✅ Get document context from uploaded files
    doc_context = uploaded_data.get("pdf", "")

    # ✅ Combine everything
    context = f"{doc_context}\n{history}"

    answer = generate_llm_answer(q.query, context)

    # ✅ Save conversation
    memory[q.session_id] = history + f"\nUser: {q.query}\nAI: {answer}"

    return {"answer": answer}