from fastapi import APIRouter

from server.agent import agent

from server.schemas.chat import ChatRequest
from server.schemas.response import ChatResponse


router = APIRouter()


@router.post(
    "/chat",
    response_model = ChatResponse
)
def chat(

    request : ChatRequest

):

    response = agent.invoke(

        {

            "messages": [

                {

                    "role": "user",

                    "content": request.message

                }

            ]

        }

    )

    answer = response["messages"][-1].content

    return ChatResponse(

        answer = answer

    )