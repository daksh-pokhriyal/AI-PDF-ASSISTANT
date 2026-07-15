from langchain.agents import create_agent
from langchain.tools import tool

from server.tools.llm import llm
from server.tools.document_router import route_document_request


@tool
def document_tool(
    request : str
) -> str:
    """
    ALWAYS use this tool for any question about the uploaded PDF.

    This tool is the ONLY source of truth for the uploaded document.

    Use this tool whenever the user:
    - asks a question about the PDF
    - asks for a summary
    - asks to explain a concept from the PDF
    - asks to compare concepts in the PDF

    Never answer from your own knowledge when the question is about the uploaded document.
    """

    return route_document_request(
        request
    )


agent = create_agent(

    model = llm,

    tools = [

        document_tool

    ]

)