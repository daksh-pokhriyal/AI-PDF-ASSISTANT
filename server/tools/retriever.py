from langchain_chroma import Chroma


def create_retriever(vector_store : Chroma):

    """
    Creates a retriever from the vector store.
    """

    retriever = vector_store.as_retriever(

        search_kwargs = {
            "k" : 4
        }

    )

    return retriever