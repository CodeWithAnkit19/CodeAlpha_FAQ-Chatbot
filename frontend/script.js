const chatArea = document.getElementById("chatArea");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");

const suggestionButtons = document.querySelectorAll(".suggestion-button");


// =========================
// Add Message to Chat
// =========================

function addMessage(message, sender) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add(
        "message",
        sender === "user"
            ? "user-message"
            : "bot-message"
    );


    const icon = document.createElement("div");

    icon.classList.add("message-icon");

    icon.textContent =
        sender === "user"
            ? "👤"
            : "🤖";


    const content = document.createElement("div");

    content.classList.add("message-content");


    const paragraph = document.createElement("p");

    paragraph.textContent = message;


    content.appendChild(paragraph);

    messageDiv.appendChild(icon);
    messageDiv.appendChild(content);

    chatArea.appendChild(messageDiv);


    // Scroll to latest message
    chatArea.scrollTop = chatArea.scrollHeight;
}


// =========================
// Send Message to Backend
// =========================

async function sendMessage() {

    const message = userInput.value.trim();

    if (!message) {
        return;
    }


    // Show user message
    addMessage(message, "user");


    // Clear input
    userInput.value = "";


    // Disable button while processing
    sendButton.disabled = true;
    sendButton.textContent = "Thinking...";


    try {

        // Send question to Flask backend
        const response = await fetch(
            "http://127.0.0.1:5000/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: message
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            addMessage(
                data.error || "Something went wrong.",
                "bot"
            );

            return;
        }


        // Show chatbot answer
        addMessage(
            data.answer,
            "bot"
        );


    } catch (error) {

        console.error("Chatbot error:", error);

        addMessage(
            "Unable to connect to the chatbot server. Please make sure the backend is running.",
            "bot"
        );

    } finally {

        // Enable button again
        sendButton.disabled = false;
        sendButton.textContent = "Send";

        userInput.focus();
    }
}


// =========================
// Send Button
// =========================

sendButton.addEventListener(
    "click",
    sendMessage
);


// =========================
// Enter Key
// =========================

userInput.addEventListener(
    "keydown",
    (event) => {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();
        }

    }
);


// =========================
// Suggested Questions
// =========================

suggestionButtons.forEach(
    (button) => {

        button.addEventListener(
            "click",
            () => {

                userInput.value =
                    button.textContent.trim();

                sendMessage();

            }
        );

    }
);