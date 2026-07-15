from langchain_core.documents import Document

from langchain_chroma import Chroma

from server.tools.embeddings import embeddings





def create_vector_store( documents : list[Document]) -> Chroma:

    """
    Creates a Chroma vector database from documents.
    """

    

    vector_store = Chroma.from_documents(

        documents = documents,

        embedding = embeddings,

        persist_directory = "vector_db"

    )

    return vector_store

