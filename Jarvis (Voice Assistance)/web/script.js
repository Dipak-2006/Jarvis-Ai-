 eel.expose(show_jarvis_response);
function show_jarvis_response(msg) {
    document.getElementById("jarvisResponse").innerText = msg;
}


async function sendCommandToJarvis(command) {
  const response = await eel.get_jarvis_response(command)();
  document.getElementById("jarvisResponse").innerText = response;
}



// Example call on load (you can hook this with mic input later)
window.onload = () => {
  setTimeout(() => {
    sendCommandToJarvis("Hello Jarvis");
  }, 1000);
};

async function sendCommandToJarvis(command) {
  console.log("Sending to backend:", command);
  const response = await eel.get_jarvis_response(command)();
  // alert("JARVIS says: " + response);
}

function listenAndSend() {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = 'en-US';
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onstart = () => {
    console.log("Listening...");
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    console.log("You said:", transcript);
    sendCommandToJarvis(transcript);
  };

  recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
    alert("Sorry, could not hear you properly.");
  };

  recognition.start();
}

document.getElementById("micButton").addEventListener("click", listenAndSend);
