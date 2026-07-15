from server.tools.summary import summarize_document
from server.tools.chat import chat_with_document


SUMMARY_KEYWORDS = [

    "summary",
    "summarize",
    "summarise",
    "overview",
    "revision notes",
    "notes"

]


def route_document_request( request : str) -> str:

    """
    Routes the user's request to the appropriate
    document feature.
    """

    request = request.lower()

    if any(

        keyword in request

        for keyword in SUMMARY_KEYWORDS

    ):

        return summarize_document()

    return chat_with_document(
        request
    )