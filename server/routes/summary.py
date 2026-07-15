from fastapi import APIRouter

from server.schemas.response import SummaryResponse

from server.tools.summary import summarize_document
from server.tools.document_session import document_session


router = APIRouter()


@router.get(

    "/summary",

    response_model = SummaryResponse

)
def summary():

    chunks = document_session.get_chunks()

    summary = summarize_document(

        chunks

    )

    return SummaryResponse(

        summary = summary

    )