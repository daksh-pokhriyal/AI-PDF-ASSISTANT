import os

from dotenv import load_dotenv
from google import genai
from PIL import Image


load_dotenv()


from pydantic import BaseModel


class ImageContent(BaseModel):

    printed_text: str

    handwritten_notes: str

    equations: list[str]

    tables: list[str]

    diagram_description: str


client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def extract_image_content(image_path: str) -> str:

    image = Image.open(image_path)

    prompt = """
    You are an expert document understanding AI.

    Extract only information useful for studying.

    1. Printed text
    2. Handwritten notes
    3. Equations
    4. Table contents

    If a diagram contains labels or important information,
    extract those labels.

    Do NOT describe colors, arrows, shapes, layout, or visual appearance unless they convey essential meaning.
    """

    response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=[
        prompt,
        image
    ],
    config={
        "response_mime_type": "application/json",
        "response_schema": ImageContent,
    }
    )   

    return response.text


# if __name__ == "__main__":

#     result = extract_image_content(
#         "temp_images/page_6_img_0.png"
#     )

#     print(result)