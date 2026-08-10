const chatMessages = document.getElementById("chatMessages");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");

let sessionId = null;

document.getElementById("marksBtn").addEventListener(
    "click",
    function() {
        sendSuggestion("What are Abhishek's marks?");
    }
);

document.getElementById("attendanceBtn").addEventListener(
    "click",
    function() {
        sendSuggestion("What is Abhishek's attendance?");
    }
);

document.getElementById("lowAttendanceBtn").addEventListener(
    "click",
    function() {
        sendSuggestion("Who has attendance below 75%?");
    }
);

function addMessage(message, sender) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add(
        "message",
        sender
    );


    const avatar = document.createElement("div");

    avatar.classList.add("avatar");

    avatar.textContent =
        sender === "assistant" ? "AI" : "You";


    const bubble = document.createElement("div");

    bubble.classList.add("bubble");

    bubble.textContent = message;


    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);

    chatMessages.appendChild(messageDiv);

    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


async function sendMessage() {

    const message =
        messageInput.value.trim();


    if (!message) {
        return;
    }


    // Show user's message
    addMessage(
        message,
        "user"
    );


    messageInput.value = "";

    sendButton.disabled = true;


    // Temporary loading message
    addMessage(
        "Thinking...",
        "assistant"
    );


    try {

        const response = await fetch(
            "http://127.0.0.1:8000/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message,
                    session_id: sessionId
                })
            }
        );


        const data = await response.json();
        sessionId = data.session_id;


        // Remove "Thinking..."
        const messages =
            document.querySelectorAll(
                ".message.assistant"
            );

        const lastMessage =
            messages[messages.length - 1];

        lastMessage.remove();


        // Display AI response
        addMessage(
            data.response,
            "assistant"
        );


    } catch (error) {

        const messages =
            document.querySelectorAll(
                ".message.assistant"
            );

        const lastMessage =
            messages[messages.length - 1];

        if (lastMessage) {
            lastMessage.remove();
        }


        addMessage(
            "⚠️ Unable to connect to the College AI server.",
            "assistant"
        );


        console.error(error);

    } finally {

        sendButton.disabled = false;

        messageInput.focus();
    }
}


function sendSuggestion(message) {

    messageInput.value = message;

    sendMessage();
}


sendButton.addEventListener(
    "click",
    sendMessage
);


messageInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {
            sendMessage();
        }

    }
);