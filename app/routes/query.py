from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm import generate_llm_answer
from app.services.rag import get_rag_answer

router = APIRouter()

memory = {}

class Query(BaseModel):
    query: str
    session_id: str
    file_text: str = ""


@router.post("/query")
def ask(q: Query):

    # 🔥 STEP 1: Get chat history (clean)
    history = memory.get(q.session_id, "")

    # 🔥 STEP 2: PRIORITY → PDF content (NOT history)
    context = ""

    if q.file_text and len(q.file_text.strip()) > 50:
        context = q.file_text[:4000]   # limit for token safety
    else:
        # fallback to RAG
        rag_data = get_rag_answer(q.query)
        context = rag_data

    # 🔥 STEP 3: Generate answer
    answer = generate_llm_answer(q.query, context)

    # 🔥 STEP 4: store minimal history (avoid pollution)
    memory[q.session_id] = f"User: {q.query}\nAI: {answer}"

    return {"answer": answer}