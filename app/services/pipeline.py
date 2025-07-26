from app.services.parser import extract_text_from_url
from app.services.chunker import chunk_text
from app.services.embedder import embed_chunks, embed_query
from app.services.vector_store import build_faiss_index, search_faiss_index
from app.services.llm_decider import answer_with_gemini
from app.services.json_formatter import format_answers
from app.models import QueryResponse

def process_query_pipeline(document_url: str, questions: list[str]) -> list[QueryResponse]:
    raw_text = extract_text_from_url(document_url)
    chunks = chunk_text(raw_text)
    chunk_embeddings = embed_chunks(chunks)
    index = build_faiss_index(chunk_embeddings)

    answers = []

    for question in questions:
        query_embedding = embed_query(question)
        top_chunks_with_scores = search_faiss_index(index, query_embedding, chunks, top_k=5)

        matched_chunks = [item["chunk"] for item in top_chunks_with_scores]
        scores = [item["score"] for item in top_chunks_with_scores]

        llm_result = answer_with_gemini(question, matched_chunks)
        
        print("Gemini response:", llm_result)

        # ✅ Extract answer string from dict
        llm_output = llm_result.get("answer", "") if isinstance(llm_result, dict) else llm_result

        answers.append(format_answers(
            query=question,
            llm_output=llm_output,
            matched_chunks=matched_chunks,
            scores=scores
        ))

    return answers
