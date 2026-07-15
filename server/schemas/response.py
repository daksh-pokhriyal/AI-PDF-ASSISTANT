from pydantic import BaseModel


class ChatResponse(BaseModel):

    answer: str


class SummaryResponse(BaseModel):

    summary: str