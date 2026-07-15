# this tool merges text from read_pdf.py and image_extractor.py
# into a single document

from server.tools.read_pdf import pdf_reader
from server.tools.image_extractor import extract_image_content


def document_merger( pdf_path : str ) -> list[dict]:

    """
    Merges text from read_pdf.py and image_extractor.py.

    Returns:
        list[dict]
    """

    pages = pdf_reader( pdf_path )

    content = [] # list of dictionaries for each page

    for page in pages:

        print(f"Processing page {page[ 'page' ]}...")

        image_contents = []

        if page[ "has_images" ]:

            for image_path in page[ "images" ]:

                image_contents.append(
                    extract_image_content( image_path )
                )

            content.append(
            {
                "page" : page[ "page" ],
                "text" : page[ "text" ],
                "image_content" : image_contents
            }
            )

            print(f"Extracted content from page {page[ 'page' ]} with images.")
        else :
            
            content.append(
            {
                "page" : page[ "page" ],
                "text" : page[ "text" ],
                "image_content" : []
            }
            )

            print(f"Extracted content from page {page[ 'page' ]} without images.")

        
    

    


    return content




# print("\n \n \n \n")

# if __name__ == "__main__":

#     result = document_merger("server/uploads/sample.pdf")

#     print(result)