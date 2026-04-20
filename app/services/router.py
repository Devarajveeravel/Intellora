from app.services.rag import get_rag_answer
from app.services.web_search import search_web
from app.services.llm import generate_llm_answer
from app.services.memory import get_history, add_message

def route_query(query: str, session_id: str):
    history = get_history(session_id)

    rag_data = get_rag_answer(query)
    web_data = search_web(query)

    context = f"""
Use the following information if relevant:

Knowledge Base:
{rag_data}

Internet:
{web_data}
"""

    # 🔥 FORCE LLM — no ugly fallback
    answer = generate_llm_answer(query, context, history)

    # 🧹 CLEAN BAD OUTPUT
    if not answer or len(answer.strip()) < 5:
        answer = "Sorry, I couldn't generate a proper answer. Please try again."

    add_message(session_id, "user", query)
    add_message(session_id, "assistant", answer)

    return answer.strip()