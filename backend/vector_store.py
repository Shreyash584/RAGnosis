import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from backend.config import EMBEDDING_MODEL, VECTOR_DB_PATH

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def save_vectors(documents):
    os.makedirs(VECTOR_DB_PATH, exist_ok=True)

    if os.path.exists(os.path.join(VECTOR_DB_PATH, "index.faiss")):
        # LOAD existing DB and ADD documents
        db = FAISS.load_local(
            VECTOR_DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
        db.add_documents(documents)
    else:
        # CREATE new DB
        db = FAISS.from_documents(documents, embeddings)

    db.save_local(VECTOR_DB_PATH)


def load_vectors():
    return FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
