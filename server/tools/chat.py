from langchain_core.documents import Document

from server.tools.llm import llm

from server.tools.document_session import document_session







def chat_with_document(query : str) -> str:

    """
    Answers a user's question using the uploaded document.
    """

    retriever = document_session.get_retriever()

    documents : list[Document] = retriever.invoke(
        query
    )

    context = ""

    for document in documents:

        context += document.page_content

        context += "\n\n"

    prompt = f"""
    You are an expert AI study assistant.

    Answer the user's question ONLY using the provided context.

    Instructions:

    - Answer accurately and clearly.
    - Do not use outside knowledge.
    - If the answer is not present in the context, reply exactly:
    "I couldn't find this information in the uploaded document."
    - If appropriate, answer using bullet points.
    - Preserve technical terms.

    Context:

    {context}

    Question:

    {query}
    """

    response = llm.invoke(
        prompt
    )

    return response.content 