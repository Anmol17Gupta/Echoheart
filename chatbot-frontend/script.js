document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");

    chatForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // Stop page refresh

        let message = userInput.value.trim();
        if (message === "") return; // Ignore empty messages

        appendMessage("user", message);
        userInput.value = ""; // Clear input field

        try {
            const response = await fetch("http://127.0.0.1:5000/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();
            appendMessage("bot", data.response);
        } catch (error) {
            console.error("Error:", error);
            appendMessage("bot", "Error connecting to chatbot.");
        }
    });

    function appendMessage(role, text) {
        let messageDiv = document.createElement("div");
        messageDiv.classList.add("message", role === "user" ? "user-message" : "bot-message");
        messageDiv.textContent = (role === "user" ? "You: " : "Bot: ") + text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight; 
    }
});
