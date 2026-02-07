import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()


def ingest_pdf():
    pdf_file_path = os.getenv("PDF_PATH")
    collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME")
    database_url = os.getenv("DATABASE_URL")

    # Carrega e divide o PDF em chunks
    loaded_documents = PyPDFLoader(pdf_file_path).load()
    chunked_documents = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    ).split_documents(loaded_documents)

    # Usa o modelo de embeddings disponível na sua conta
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    vector_store = PGVector(
        embeddings=embeddings_model,
        collection_name=collection_name,
        connection=database_url,
        use_jsonb=True
    )

    # Enriquecimento dos documentos
    enriched_documents = [
        Document(
            page_content=doc.page_content,
            metadata={
                key: value
                for key, value in doc.metadata.items()
                if value not in ("", None)
            }
        )
        for doc in chunked_documents
    ]

    # Processa em lotes menores para não estourar quota
    batch_size = 5

    for start_index in range(0, len(enriched_documents), batch_size):
        document_batch = enriched_documents[start_index:start_index + batch_size]

        batch_ids = [
            f"doc-{start_index + offset}"
            for offset in range(len(document_batch))
        ]

        vector_store.add_documents(
            documents=document_batch,
            ids=batch_ids
        )

        # pausa curta para respeitar RPM/TPM
        time.sleep(2)


if __name__ == "__main__":
    ingest_pdf()
