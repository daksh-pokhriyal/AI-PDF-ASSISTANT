# step by step how i created this project 



# 1. making of new environment

uv venv
source .venv/bin/activate

make requirements.txt

and .env file

# 2. make tool




1. read_pdf

why did'nt i made this a tool ??

=> 
Rule of thumb

A function should be a LangChain tool only if you expect the agent to decide when to call it.

Ask yourself:

Will the agent ever choose whether or not to read the PDF?

The answer is no.



# read_pdf tool output :-

[
    {
        "page": 1,
        "text": "Machine Learning is a subset of AI.",
        "images": [
            "temp_images/page_1_img_1.png"
        ],
        "has_text": True,
        "has_images": True
    }
]


# image_extractor tool output :-


{
  "printed_text": "",
  "handwritten_notes": "",
  "equations": [],
  "tables": [],
  "diagram_description": "A 2D line plot displays a straight blue line on a Cartesian coordinate system. The x-axis is labeled with tick marks at -10.0, -7.5, -5.0, -2.5, 0.0, 2.5, 5.0, and 7.5. The y-axis is labeled with tick marks at -10.0, -7.5, -5.0, -2.5, 0.0, 2.5, 5.0, and 7.5. The blue line extends from the bottom-left of the plot, approximately at coordinates (-10, -10), diagonally upwards to the top-right, approximately at coordinates (9, 9)."
}

# document_merger tool :-

it combines both the outputs of the abouve tools and its output look like

{
    text : ""
    image_content : 

                        "printed_text": "",
                        "handwritten_notes": "",
                        "equations": [],
                        "tables": [],
                        "diagram_description": "A 2D line plot displays a straight blue line on                     a Cartesian coordinate system. The x-axis is labeled with tick marks at                     -10.0, -7.5, -5.0, -2.5, 0.0, 2.5, 5.0, and 7.5. The y-axis is labeled                  with tick marks at -10.0, -7.5, -5.0, -2.5, 0.0, 2.5, 5.0, and 7.5. The                     blue line extends from the bottom-left of the plot, approximately at                coordinates (-10, -10), diagonally upwards to the top-right,              approximately at coordinates (9, 9)."
}



# for now these are three tools or functions , they extract data from pdf , so now our RAG part starts :-


# chunker.py


firstly we have to convert list to dict to list of documents 

then we chunks data

chunker.py should do only one thing:

Convert the merged document into LangChain Document objects and split them into chunks.

It should not:

❌ Create embeddings
❌ Store in Chroma
❌ Call Gemini
❌ Retrieve anything




it will have an output of list of Documents 

Document contains page_content and Metadata


# now theres come a problem that gemini api only limit 5 images to process per minute 


# Embeddings.py

Responsibility

embeddings.py should do only one thing:

Create an embedding model.

It should not:

❌ Store vectors
❌ Retrieve vectors
❌ Query the database

Those belong to the vector store.

# vector_store.py



# summarizer tool


User Query

↓

Retriever.invoke()

↓

Top Chunks

↓

Combine Chunks

↓

Gemini

↓

Summary



Two different summarization modes:


1. Full Document Summary

Chunks

↓

Gemini

↓

Summary

This summarizes the entire document (or processes it in batches if it's large).

2. Question Answering / Topic Summary
User:
Summarize the chapter on RNNs

↓

Retriever

↓

Relevant Chunks

↓

Gemini

↓

Answer

This uses RAG because the user is asking about a specific topic.





# in full summary - 
# summary.py

- it uses heirarchiel summary 

Chunks

↓

Group 1
Group 2
Group 3
...

↓

Gemini

↓

Mini Summary 1
Mini Summary 2
Mini Summary 3
...

↓

Combine Mini Summaries

↓

Gemini

↓

Final Summary


# chat.py


User Question

↓

Retriever

↓

Relevant Chunks

↓

Gemini

↓

Answer


# app.py 

this is the main file 

# now for each pdf only process PDF one time and store data in cache 
# and then ask ques from agent


Upload PDF
      │
      ▼
Process PDF
      │
      ▼
Keep in Memory
      │
      ├──────────────┐
      ▼              ▼
Chunks         Retriever
      │              │
      └──────┬───────┘
             ▼
         Agent / API


# FLOW 


Application Starts

↓

load_document()

↓

Chunks stored

↓

Retriever stored

↓

User asks Question 1

↓

Chat

↓

User asks Question 2

↓

Chat

↓

User asks Question 3

↓

Summary

↓

No preprocessing again


# agent.py

User

↓

Agent

↓

Should I...

┌───────────────┐
│Summarize PDF? │──────► summary.py
└───────────────┘

┌───────────────┐
│Answer Question│──────► chat.py
└───────────────┘



# python -m server.app


# fast API


#                    1. High-Level Architecture



                          USER
                            │
                            ▼
                    React Frontend
                            │
                 HTTP Requests (REST API)
                            │
                            ▼
                  ┌────────────────────┐
                  │      FastAPI       │
                  └────────────────────┘
                     │      │       │
                     │      │       │
          POST /upload   POST /chat   GET /summary
                     │      │       │
                     ▼      ▼       ▼
             document_session   agent   summarize_document()
                     │
                     ▼
          ┌─────────────────────────┐
          │     DocumentSession     │
          └─────────────────────────┘
               │      │        │
               │      │        │
          Chunks  Retriever  Vector Store



#                    2. Upload flow


                    Upload PDF
                         │
                         ▼
                POST /upload
                         │
                         ▼
             Save PDF in uploads/
                         │
                         ▼
        document_session.load_document()
                         │
                         ▼
                 document_merger()
                         │
         ┌───────────────┴────────────────┐
         │                                │
         ▼                                ▼
     read_pdf.py                 image_extractor.py
         │                                │
         └───────────────┬────────────────┘
                         ▼
               merged_document (list[dict])
                         │
                         ▼
               create_documents()
                         │
                         ▼
               chunk_documents()
                         │
                         ▼
             HuggingFaceEmbeddings
                         │
                         ▼
                     Chroma DB
                         │
                         ▼
                 create_retriever()
                         │
                         ▼
          Stored inside document_session




#                  3. Chat Flow


                   React
                      │
                      ▼
                 POST /chat
                      │
                      ▼
                agent.invoke()
                      │
                      ▼
              Mistral Agent
                      │
        Decides whether to use tool
                      │
                      ▼
               document_tool()
                      │
                      ▼
          route_document_request()
                      │
                      ▼
           chat_with_document()
                      │
                      ▼
 document_session.get_retriever()
                      │
                      ▼
             Retriever.invoke()
                      │
                      ▼
          Top-K Relevant Chunks
                      │
                      ▼
         Build Context Prompt
                      │
                      ▼
               Mistral LLM
                      │
                      ▼
               Final Answer
                      │
                      ▼
                 FastAPI
                      │
                      ▼
                    React



#                   4. Summary Flow


                 React
                    │
                    ▼
             GET /summary
                    │
                    ▼
        summarize_document()
                    │
                    ▼
 document_session.get_chunks()
                    │
                    ▼
        Hierarchical Summarization
                    │
                    ▼
             Final Summary
                    │
                    ▼
                FastAPI
                    │
                    ▼
                  React



# uvicorn server.main:app --reload











