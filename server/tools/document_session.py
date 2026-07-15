from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_chroma import Chroma

from server.tools.document_merger import document_merger
from server.tools.chunker import create_documents, chunk_documents
from server.tools.vector_store import create_vector_store
from server.tools.retriever import create_retriever

import os
import shutil


class DocumentSession:

    def __init__( self ):

        self.chunks : list[Document] | None = None

        self.vector_store : Chroma | None = None

        self.retriever : BaseRetriever | None = None


    def load_document( self, pdf_path : str ) -> None:

        """
        Process the uploaded PDF and create the RAG pipeline.
        """

        print( "Reading PDF..." )

        # ---------- Clear old temp images ----------

        if os.path.exists("temp_images"):

            shutil.rmtree("temp_images")

        os.makedirs("temp_images")


        # ---------- Clear old vector database ----------

        if os.path.exists("vector_db"):

            shutil.rmtree("vector_db")

        merged_document = document_merger(
            pdf_path
        )

        print( "Creating Documents..." )

        documents = create_documents(
            merged_document
        )

        print( "Chunking Documents..." )

        self.chunks = chunk_documents(
            documents
        )

        print( "Creating Vector Store..." )

        self.vector_store = create_vector_store(
            self.chunks
        )

        print( "Creating Retriever..." )

        self.retriever = create_retriever(
            self.vector_store
        )

        print( "Document Loaded Successfully." )


    def get_chunks( self ) -> list[Document]:

        if self.chunks is None:

            raise ValueError(
                "No document has been loaded."
            )

        return self.chunks


    def get_retriever( self ) -> BaseRetriever:

        if self.retriever is None:

            raise ValueError(
                "No document has been loaded."
            )

        return self.retriever


    def get_vector_store( self ) -> Chroma:

        if self.vector_store is None:

            raise ValueError(
                "No document has been loaded."
            )

        return self.vector_store


document_session = DocumentSession()