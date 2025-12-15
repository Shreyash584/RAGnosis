import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def load_pdf(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    for d in docs:
        d.metadata["source"] = pdf_path
        d.metadata["type"] = "pdf"
    return docs


def load_web(url: str):
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10
    )

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove noise
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    article = soup.find("article")
    text = (
        article.get_text(separator=" ", strip=True)
        if article else soup.get_text(separator=" ", strip=True)
    )

    return [
        Document(
            page_content=text,
            metadata={"source": url, "type": "web"}
        )
    ]


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    return splitter.split_documents(documents)
