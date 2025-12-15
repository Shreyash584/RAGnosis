import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from backend.vector_store import load_vectors
from backend.config import LLM_MODEL, VECTOR_DB_PATH


llm = OllamaLLM(model=LLM_MODEL, temperature=0)


PROMPT = ChatPromptTemplate.from_template(
    """
You are a retrieval-based assistant.

You MUST answer using ONLY the provided context.
If the answer is not present, say exactly:
"I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""
)


def format_docs(docs):
    formatted = []
    for d in docs:
        src = d.metadata.get("source", "unknown")
        formatted.append(f"[SOURCE: {src}]\n{d.page_content}")
    return "\n\n".join(formatted)


def get_qa_chain():
    if not os.path.exists(VECTOR_DB_PATH):
        raise RuntimeError(
            "Vector database not found. Please ingest PDFs or URLs first."
        )

    db = load_vectors()
    retriever = db.as_retriever(search_kwargs={"k": 4})

    return (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | PROMPT
        | llm
        | StrOutputParser()
    )
