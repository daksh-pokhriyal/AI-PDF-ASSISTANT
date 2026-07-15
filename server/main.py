from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.routes.upload import router as upload_router
from server.routes.chat import router as chat_router
from server.routes.summary import router as summary_router


app = FastAPI(

    title="PRIME AI",

    version="1.0.0"

)


app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://127.0.0.1:5500",

        "http://localhost:5500"

    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


app.include_router(

    upload_router

)

app.include_router(

    chat_router

)

app.include_router(

    summary_router

)


@app.get("/")
def home():

    return {

        "message": "PRIME AI Backend Running"

    }