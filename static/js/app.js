const pdfInput = document.getElementById("pdfInput");

const uploadStatus =
    document.getElementById("uploadStatus");

const questionInput =
    document.getElementById("questionInput");

const chatMessages =
    document.getElementById("chatMessages");

const resultCard =
    document.getElementById("resultCard");

const resultContent =
    document.getElementById("resultContent");


// =========================
// PDF UPLOAD
// =========================

pdfInput.addEventListener("change", async function () {

    const file = this.files[0];

    if (!file) {
        return;
    }

    if (!file.name.toLowerCase().endsWith(".pdf")) {

        uploadStatus.innerText =
            "Please select a PDF file.";

        return;
    }

    uploadStatus.innerText =
        "Uploading and processing PDF...";

    const formData = new FormData();

    formData.append("pdf", file);

    try {

        const response = await fetch(
            "/upload",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (data.success) {

            uploadStatus.innerText =
                `✓ ${data.filename} uploaded successfully — ${data.characters} characters extracted.`;

            const pdfStatus =
                document.getElementById("pdfStatus");

            if (pdfStatus) {
                pdfStatus.innerText = "Ready ✓";
            }

        } else {

            uploadStatus.innerText =
                data.message || "Upload failed.";

        }

    } catch (error) {

        console.error("UPLOAD ERROR:", error);

        uploadStatus.innerText =
            "Upload failed. Please try again.";

    }

});


// =========================
// ASK QUESTION
// =========================

async function askQuestion() {

    const question =
        questionInput.value.trim();

    if (!question) {
        return;
    }

    addMessage(
        "You",
        question,
        "user"
    );

    questionInput.value = "";

    addMessage(
        "StudyPDF AI",
        "Thinking...",
        "ai"
    );

    try {

        const response = await fetch(
            "/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );

        const data =
            await response.json();

        const messages =
            document.querySelectorAll(
                ".message.ai"
            );

        if (messages.length > 0) {

            const lastMessage =
                messages[messages.length - 1];

            const messageText =
                lastMessage.querySelector(
                    ".message-text"
                );

            if (data.success) {

                messageText.innerHTML =
                    marked.parse(data.answer);

            } else {

                messageText.innerText =
                    data.answer ||
                    "Something went wrong.";

            }

        }

    } catch (error) {

        console.error("ASK ERROR:", error);

        const messages =
            document.querySelectorAll(
                ".message.ai"
            );

        if (messages.length > 0) {

            messages[
                messages.length - 1
            ].querySelector(
                ".message-text"
            ).innerText =
                "Something went wrong. Please try again.";

        }

    }

}


// =========================
// ADD MESSAGE
// =========================

function addMessage(
    sender,
    text,
    type
) {

    const message =
        document.createElement("div");

    message.className =
        `message ${type}`;

    message.style.marginBottom =
        "15px";

    message.style.padding =
        "14px";

    message.style.borderRadius =
        "12px";

    message.style.background =
        type === "user"
            ? "#eeeaff"
            : "#f7f5fc";

    message.innerHTML = `
        <strong>${sender}</strong>
        <div class="message-text"
             style="margin-top:6px;">
            ${text}
        </div>
    `;

    chatMessages.appendChild(message);

    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


// =========================
// SUMMARY
// =========================

async function generateSummary() {

    await runTool(
        "/summary",
        "Generating your summary..."
    );

}


// =========================
// 2 MARK
// =========================

async function generateTwoMark() {

    await runTool(
        "/two-mark",
        "Generating 2-mark questions..."
    );

}


// =========================
// 16 MARK
// =========================

async function generateSixteenMark() {

    await runTool(
        "/sixteen-mark",
        "Generating 16-mark questions..."
    );

}


// =========================
// IMPORTANT QUESTIONS
// =========================

async function generateImportantQuestions() {

    await runTool(
        "/important-questions",
        "Finding important questions..."
    );

}


// =========================
// TOOL HANDLER
// =========================

async function runTool(
    endpoint,
    loadingText
) {

    showLoading(loadingText);

    try {

        const response =
            await fetch(
                endpoint,
                {
                    method: "POST"
                }
            );

        const data =
            await response.json();

        if (data.success) {

            resultContent.innerHTML =
                marked.parse(
                    data.answer
                );

        } else {

            resultContent.innerText =
                data.answer ||
                data.message ||
                "Something went wrong.";

        }

    } catch (error) {

        console.error(
            "TOOL ERROR:",
            error
        );

        resultContent.innerText =
            "Something went wrong. Please try again.";
    }

}


// =========================
// LOADING
// =========================

function showLoading(
    message = "AI is thinking..."
) {

    resultCard.classList.remove(
        "hidden"
    );

    resultContent.innerHTML = `
        <div class="ai-thinking">
            <div class="ai-spinner"></div>
            <span>${message}</span>
        </div>
    `;

}


// =========================
// QUESTION ENTER KEY
// =========================

questionInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            askQuestion();

        }

    }
);


// =========================
// FOCUS QUESTION
// =========================

function focusQuestion() {

    questionInput.focus();

    questionInput.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });

}


// =========================
// CLOSE RESULT
// =========================

function closeResult() {

    resultCard.classList.add(
        "hidden"
    );

}
