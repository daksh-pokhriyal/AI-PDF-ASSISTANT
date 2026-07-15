const summaryButton = document.getElementById(

    "summary-btn"

);

const summaryContainer = document.getElementById(

    "summary-container"

);


summaryButton.addEventListener(

    "click",

    generateSummary

);


async function generateSummary(){

    summaryButton.disabled = true;

    summaryButton.textContent =

        "Generating...";


    summaryContainer.innerHTML = `

        <div class="loader"></div>

        <br>

        <p>

            Generating Summary...

        </p>

    `;


    try{

        const response = await fetch(

            "http://127.0.0.1:8000/summary"

        );


        if(!response.ok){

            throw new Error(

                "Failed to generate summary."

            );

        }


        const data = await response.json();


        summaryContainer.innerHTML =
    marked.parse(
        data.summary
    );

document.querySelectorAll(

    "pre code"

).forEach(

    (block)=>{

        hljs.highlightElement(

            block

        );

    }

);


    }

    catch(error){

        console.error(error);

        summaryContainer.innerHTML =

            "<p>❌ Failed to generate summary.</p>";

    }

    finally{

        summaryButton.disabled = false;

        summaryButton.textContent =

            "Generate Summary";

    }

}