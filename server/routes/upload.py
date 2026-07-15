from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File

from server.tools.document_session import document_session


router = APIRouter()


UPLOAD_FOLDER = Path("server/uploads")

UPLOAD_FOLDER.mkdir(
    exist_ok = True
)


@router.post("/upload")
def upload_pdf(

    file : UploadFile = File(...)

):

    if file.content_type != "application/pdf":

        return {

            "error" : "Only PDF files are allowed."

        }

    pdf_path = UPLOAD_FOLDER / file.filename

    with open(pdf_path, "wb") as pdf:

        shutil.copyfileobj(
            file.file,
            pdf
        )

    document_session.load_document(
        str(pdf_path)
    )

    return {

        "message" : "PDF uploaded successfully.",

        "filename" : file.filename

    }