from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI

load_dotenv()

llm = ChatMistralAI(
    model="mistral-medium-latest",
    temperature=0
)

# response = llm.invoke("are you a human")

# print(response.content)