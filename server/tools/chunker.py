from langchain_core.documents import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter


# in this tool, first we have a function which converts list of 
# dictionaries into langchain documents, 
# and then we have a function which splits the documents 
# into smaller chunks


def create_documents (merged_content : list[dict]) -> list[Document]:

    """
    Converts the merged document into LangChain Documents.

    Returns:
        list[Document]
    """

    documents=[]

    for page in merged_content:

        page_content= page['text']

        if page['image_content']:

            for image_content in page['image_content']:

                page_content+= "\n\n" + image_content

        
        documents.append(

            Document(
                page_content = page_content,

                metadata ={
                    'page' : page['page']
                }

            
            )
        )

    return documents


# print("\n \n \n \n")

# if __name__ == "__main__":

#     result = create_documents("server/uploads/sample.pdf")

#     print(result)



def chunk_documents(documents : list[Document]) -> list[Document]:

    """
    split the documents into smaller chunks using RecursiveCharacterTextSplitter.
    """

    text_splitter= RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators = [
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]

    )

    chunks= text_splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):

        chunk.metadata["chunk_id"] = index

    return chunks




















