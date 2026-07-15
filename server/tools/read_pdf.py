import fitz
import os


"""
    Reads a PDF and extracts:
    - Text from each page
    - Images from each page

    Returns:
        List[dict]

"""


def pdf_reader(pdf_path: str) -> list:

    pages = [] # list of dictionaries for each page

    document = fitz.open(pdf_path)

    os.makedirs("temp_images", exist_ok=True)

    for page_number in range(len(document)):

        page=document[page_number]

        text = page.get_text().strip()

        image_paths = []

        image_list = page.get_images(full=True)

        for image_number in range(len(image_list)):

            image=image_list[image_number]
            

            xref = image[0]

            image_data = document.extract_image(xref)

            image_bytes = image_data["image"]

            image_extension = image_data["ext"]

            image_path = (
                f"temp_images/page_{page_number}_img_{image_number}.{image_extension}"
            )

            with open(image_path, "wb") as file:

                file.write(image_bytes)

            image_paths.append(image_path)

        pages.append(
            {
                "page": page_number,
                "text": text,
                "images": image_paths,
                "has_text": bool(text),
                "has_images": len(image_paths) > 0,
            }
        )

    document.close()

    return pages





# q=pdf_reader('server/uploads/sample.pdf')
# print("\n \n \n \n")
# print(q[1])
