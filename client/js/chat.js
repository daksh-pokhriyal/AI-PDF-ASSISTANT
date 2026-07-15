const chatInput = document.getElementById("chat-input");

const sendButton = document.getElementById("send-btn");

const chatContainer = document.getElementById("chat-container");


sendButton.addEventListener(

    "click",

    sendMessage

);


chatInput.addEventListener(

    "keydown",

    (event)=>{

        if(event.key==="Enter"){

            sendMessage();

        }

    }

);


function addMessage(

    message,

    sender

){

    const messageDiv = document.createElement(

        "div"

    );

    messageDiv.classList.add(

        "message",

        sender

    );

    const bubble = document.createElement(

        "div"

    );

    bubble.classList.add(

        "bubble"

    );

    bubble.textContent = message;

    messageDiv.appendChild(

        bubble

    );

    chatContainer.appendChild(

        messageDiv

    );

    chatContainer.scrollTop =

        chatContainer.scrollHeight;

}


async function sendMessage(){

    const question =

        chatInput.value.trim();

    if(question===""){

        return;

    }

    addMessage(

        question,

        "user"

    );

    chatInput.value="";



    const thinkingDiv = document.createElement(

        "div"

    );

    thinkingDiv.classList.add(

        "message",

        "ai"

    );



    const thinkingBubble = document.createElement(

        "div"

    );

    thinkingBubble.classList.add(

        "bubble"

    );



    thinkingBubble.textContent =

        "Thinking...";



    thinkingDiv.appendChild(

        thinkingBubble

    );



    chatContainer.appendChild(

        thinkingDiv

    );



    chatContainer.scrollTop =

        chatContainer.scrollHeight;



    try{

        const response = await fetch(

            "http://127.0.0.1:8000/chat",

            {

                method:"POST",

                headers:{

                    "Content-Type":"application/json"

                },

                body:JSON.stringify(

                    {

                        message:question

                    }

                )

            }

        );



        const data = await response.json();



        thinkingBubble.innerHTML =
    marked.parse(
        data.answer
    );

thinkingBubble.querySelectorAll(

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

        console.error(

            error

        );



        thinkingBubble.textContent =

            "Server Error.";

    }

}