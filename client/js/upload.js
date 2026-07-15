const fileInput = document.getElementById("file-input");

const uploadButton = document.getElementById("upload-btn");

const pdfName = document.getElementById("pdf-name");

const uploadBox = document.getElementById("upload-box");

const uploadStatus = document.getElementById("upload-status");


uploadButton.addEventListener(

    "click",

    uploadPDF

);


async function uploadPDF(){

    const file = fileInput.files[0];

    if(!file){

        alert("Please choose a PDF.");

        return;

    }

    pdfName.textContent = file.name;

    uploadButton.disabled = true;

    uploadButton.textContent = "Uploading...";


    const formData = new FormData();

    formData.append(

        "file",

        file

    );

    try{

        const response = await fetch(

            "http://127.0.0.1:8000/upload",

            {

                method:"POST",

                body:formData

            }

        );

        const data = await response.json();

        if(response.ok){

           uploadStatus.innerHTML = "✅ PDF uploaded successfully!";

    pdfName.innerHTML = `
    📄 ${file.name}
    <br>
    <span style="color:#22C55E;">
    Ready for Chat
    </span>
    `;

        }

        else{

            uploadStatus.innerHTML = "❌ Upload Failed";

        }

    }

    catch(error){

        console.error(error);

        uploadStatus.innerHTML = "❌ Server Error";

    }

    finally{

    uploadButton.disabled = true;

    uploadButton.textContent = "Processing...";

    uploadStatus.innerHTML = "⏳ Processing PDF...";

    }

}