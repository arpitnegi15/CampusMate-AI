const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");

function addMessage(message, sender) {
    const div = document.createElement("div");
    div.className = sender === "user" ? "user-message" : "bot-message";
    div.textContent = message;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
    return div;
}

function sendQuick(text) {
    userInput.value = text;
    sendMessage();
}
function speakAnswer(text) {
    const box = document.getElementById("voiceAnswer");
    if (!box || !box.checked) return;
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const voice = new SpeechSynthesisUtterance(text);
    voice.lang = 'en-IN';
    voice.rate = 1.0;
    window.speechSynthesis.speak(voice);
}
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (message === "") return;
    addMessage(message, "user");
    userInput.value = "";

    // Show typing for 2 seconds - looks real
    const typingDiv = addMessage("CampusMate is typing...", "bot");
    await sleep(2000);

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });
        const data = await response.json();
        typingDiv.remove();
        addMessage(data.reply, "bot");
        speakAnswer(data.reply);
    } catch (e) {
        typingDiv.remove();
        addMessage("Server is OFF. Start app.py in terminal.", "bot");
    }
}