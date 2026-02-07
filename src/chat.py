import os
from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_postgres import PGVector
from search import search_prompt

load_dotenv()


def _create_vector_store():
    collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME")
    database_url = os.getenv("DATABASE_URL")

    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    vector_store = PGVector(
        embeddings=embeddings_model,
        collection_name=collection_name,
        connection=database_url,
        use_jsonb=True
    )

    return vector_store


def _search_vector_store(user_query):
    vector_store = _create_vector_store()
    search_results = vector_store.similarity_search_with_score(
        user_query,
        k=10
    )
    return search_results


def main():
    chat_model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    chain = search_prompt() | chat_model

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    print("Assistente iniciado com sucesso.")
    print("Digite sua pergunta com base nos documentos carregados.")
    print("Pressione ENTER sem digitar nada para encerrar.")
    print("-" * 60)

    while True:
        user_question = input("Pergunta: ")

        if not user_question:
            print("Sessão encerrada. Obrigado por utilizar o assistente.")
            break

        context_documents = _search_vector_store(user_question)
        response = chain.invoke(
            {
                "contexto": context_documents,
                "pergunta": user_question
            }
        )

        print("\nResposta:")
        print(response.content)

        print("-" * 60)


if __name__ == "__main__":
    main()
