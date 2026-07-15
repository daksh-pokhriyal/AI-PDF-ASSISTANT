from server.agent import agent
from server.tools.document_session import document_session


PDF_PATH = "server/uploads/sample_2.pdf"

document_session.load_document(
    PDF_PATH
)

response = agent.invoke(

    {
        "messages": [

            {
                "role": "user",

                "content": "Answer only using the uploaded PDF. "
                "What is temperature in LLM generation and how does it affect output? "
                
            }

        ]

    }

)

print(
    response["messages"][-1].content
)

