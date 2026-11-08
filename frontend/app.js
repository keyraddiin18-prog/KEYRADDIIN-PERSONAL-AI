/* ==========================================
   KEYRADDIIN PERSONAL AI
   JAVASCRIPT CHAT ENGINE
   Version 1.0
========================================== */

const chatArea = document.getElementById("chatArea");
const messages = document.getElementById("messages");
const welcomeScreen = document.getElementById("welcomeScreen");

const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const sidebar = document.getElementById("sidebar");

let chatMessages = [];
let isSending = false;


// ==========================================
// 1. SEND MESSAGE
// ==========================================

async function sendMessage() {

    const message = userInput.value.trim();

    if (!message || isSending) return;

    isSending = true;

    welcomeScreen.style.display = "none";

    // Display user message
    addMessage(message, "user");

    chatMessages.push({
        role: "user",
        content: message
    });

    userInput.value = "";
    userInput.style.height = "auto";

    sendButton.disabled = true;

    // Temporary development response
    showDevelopmentMessage();

}


// ==========================================
// 2. ADD MESSAGE
// ==========================================

function addMessage(text, sender) {

    const messageDiv = document.createElement("div");

    messageDiv.className = "message " + sender;

    const avatar = document.createElement("div");

    avatar.className = "message-avatar";

    avatar.textContent = sender === "user" ? "K" : "AI";

    const content = document.createElement("div");

    content.className = "message-content";

    const name = document.createElement("div");

    name.className = "message-name";

    name.textContent =
        sender === "user"
        ? "YOU"
        : "KEYRADDIIN PERSONAL AI";

    const textContent = document.createElement("div");

    // Securely display text
    textContent.textContent = text;

    content.appendChild(name);
    content.appendChild(textContent);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);

    messages.appendChild(messageDiv);

    scrollToBottom();

}


// ==========================================
// 3. DEVELOPMENT MESSAGE
// ==========================================

function showDevelopmentMessage() {

    setTimeout(() => {

        const response =
        "Interface test successful! ✓\n\n" +
        "KEYRADDIIN PERSONAL AI frontend is working.\n\n" +
        "The real AI connection will be activated " +
        "after we connect the Python Backend and Gemini API.\n\n" +
        "Frontend Status: ONLINE\n" +
        "AI Backend Status: NOT CONNECTED YET";

        addMessage(response, "assistant");

        chatMessages.push({
            role: "assistant",
            content: response
        });

        isSending = false;

        sendButton.disabled = false;

    }, 600);

}


// ==========================================
// 4. NEW CHAT
// ==========================================

function newChat() {

    const confirmNew = confirm(
        "Start a new conversation?"
    );

    if (!confirmNew) return;

    messages.innerHTML = "";

    chatMessages = [];

    welcomeScreen.style.display = "block";

    userInput.value = "";

    userInput.focus();

    closeSidebar();

}


// ==========================================
// 5. SUGGESTIONS
// ==========================================

function useSuggestion(text) {

    userInput.value = text;

    sendMessage();

}


// ==========================================
// 6. ENTER KEY SUPPORT
// ==========================================

userInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();

    }

});


// ==========================================
// 7. TEXTAREA AUTO RESIZE
// ==========================================

userInput.addEventListener("input", function() {

    this.style.height = "auto";

    this.style.height =
        Math.min(this.scrollHeight, 150) + "px";

});


// ==========================================
// 8. SIDEBAR
// ==========================================

function toggleSidebar() {

    sidebar.classList.toggle("open");

}


function closeSidebar() {

    sidebar.classList.remove("open");

}


// ==========================================
// 9. SCROLL TO BOTTOM
// ==========================================

function scrollToBottom() {

    setTimeout(() => {

        chatArea.scrollTo({
            top: chatArea.scrollHeight,
            behavior: "smooth"
        });

    }, 100);

}


// ==========================================
// 10. INITIALIZATION
// ==========================================

document.addEventListener("DOMContentLoaded", function() {

    console.log(
        "KEYRADDIIN PERSONAL AI initialized successfully."
    );

});

console.log("KEYRADDIIN PERSONAL AI v1.0");