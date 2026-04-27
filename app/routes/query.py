from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm import generate_llm_answer
from app.routes.upload import uploaded_data

router = APIRouter()

memory = {}

class Query(BaseModel):
    query: str
    session_id: str


@router.post("/query")
def ask(q: Query):
    history = memory.get(q.session_id, "")

    pdf_text = uploaded_data.get("pdf", "")

    print("PDF LENGTH:", len(pdf_text))

    context = f"{pdf_text}\n{history}"

    answer = generate_llm_answer(q.query, context)

    memory[q.session_id] = history + f"\nUser: {q.query}\nAI: {answer}"

    return {"answer": answer}