
const recordBtn = document.getElementById("record");
const statusText = document.getElementById("status");
const responseText = document.getElementById("response");

recordBtn.addEventListener("click", () => {
    const activateMsg = new SpeechSynthesisUtterance("Jarvis activated, I'm listening...");
    window.speechSynthesis.speak(activateMsg);

    if (!navigator.mediaDevices) {
        alert("Your browser doesn't support audio recording.");
        return;
    }

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            const chunks = [];

            mediaRecorder.ondataavailable = e => chunks.push(e.data);
            mediaRecorder.onstop = () => {
                const blob = new Blob(chunks, { type: "audio/wav" });
                const formData = new FormData();
                formData.append("audio", blob, "speech.wav");

                fetch("/process", { method: "POST", body: formData })
                    .then(res => res.json())
                    .then(data => {
                        responseText.innerText = data.response;
                        const responseMsg = new SpeechSynthesisUtterance(data.response);
                        window.speechSynthesis.speak(responseMsg);
                        statusText.innerText = "Press the mic and speak...";
                    })
                    .catch(() => {
                        statusText.innerText = "Error sending audio.";
                    });
            };

            mediaRecorder.start();
            statusText.innerText = "Recording... Release mic to send.";

            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000);
        })
        .catch(() => alert("Microphone access denied."));
});
