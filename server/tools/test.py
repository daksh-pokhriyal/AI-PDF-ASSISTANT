from server.tools.document_merger import document_merger
from server.tools.chunker import create_documents, chunk_documents


# ----------------------------------------------------------------
# this is artificial data to test the chunking functionality.

from langchain_core.documents import Document

documents = [

    Document(

        page_content = """
Machine Learning is a subset of Artificial Intelligence.

It enables computers to learn patterns from data without being explicitly programmed.

Handwritten Notes:

- Very Important for Exam
- Revise supervised learning

Equation:

Loss = (Prediction - Actual)^2

""",

        metadata = {
            "page" : 1
        }

    ),

    Document(

        page_content = """
Artificial Neural Networks (ANN)

ANNs consist of an input layer, hidden layers and an output layer.

Handwritten Notes:

- ANN cannot remember previous inputs.
- Suitable for fixed-size input.

""",

        metadata = {
            "page" : 2
        }

    ),

    Document(

        page_content = """
Recurrent Neural Networks (RNN)

RNNs introduce memory by passing hidden states across time steps.

Problems:

- Vanishing Gradient
- Exploding Gradient

Handwritten Notes:

LSTM and GRU solve the vanishing gradient problem.

Equation:

h_t = f(h_(t-1), x_t)

""",

        metadata = {
            "page" : 3
        }

    ),

    Document(

        page_content = """
Encoder Decoder Architecture

Encoder converts an input sequence into a context vector.

Decoder generates the output sequence.

Diagram Information:

Encoder -> Context Vector -> Decoder

Teacher Forcing is used during training.

""",

        metadata = {
            "page" : 4
        }

    )

]


# ----------------------------------------------------------------



chunks = chunk_documents(
    documents
)





from server.tools.vector_store import create_vector_store

vector_store = create_vector_store(
    chunks
)

print("Vector Store Created Successfully")

from retriever import create_retriever

retriever = create_retriever(
    vector_store
)

results = retriever.invoke(
    "What is an Encoder?"
)

for document in results:

    print("=" * 50)

    print(document.page_content)

    print(document.metadata)
