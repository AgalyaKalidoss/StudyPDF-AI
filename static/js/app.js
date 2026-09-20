// =====================================================
// ELEMENTS
// =====================================================

const pdfInput =
    document.getElementById("pdfInput");

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


// =====================================================
// PDF UPLOAD
// =====================================================

if (pdfInput) {

    pdfInput.addEventListener(
        "change",
        async function () {

            const file =
                this.files[0];


            if (!file) {
                return;
            }


            if (
                !file.name
                    .toLowerCase()
                    .endsWith(".pdf")
            ) {

                uploadStatus.innerText =
                    "Please select a PDF file.";

                return;
            }


            uploadStatus.innerText =
                "Uploading and processing PDF...";


            const formData =
                new FormData();


            formData.append(
                "pdf",
                file
            );


            try {

                const response =
                    await fetch(
                        "/upload",
                        {
                            method: "POST",
                            body: formData
                        }
                    );


                const data =
                    await response.json();


                if (data.success) {

                    uploadStatus.innerText =
                        `✓ ${data.filename} uploaded successfully — ${data.characters} characters extracted.`;


                    const pdfStatus =
                        document.getElementById(
                            "pdfStatus"
                        );


                    if (pdfStatus) {

                        pdfStatus.innerText =
                            "Ready ✓";

                    }

                } else {

                    uploadStatus.innerText =
                        data.message ||
                        "Upload failed.";

                }


            } catch (error) {

                console.error(
                    "UPLOAD ERROR:",
                    error
                );


                uploadStatus.innerText =
                    "Upload failed. Please try again.";

            }

        }
    );

}


// =====================================================
// ASK QUESTION
// =====================================================

async function askQuestion() {

    if (!questionInput) {
        return;
    }


    const question =
        questionInput.value.trim();


    if (!question) {
        return;
    }


    // Add user message
    addMessage(
        "You",
        question,
        "user"
    );


    questionInput.value = "";


    // Add temporary AI message
    addMessage(
        "StudyPDF AI",
        "Thinking...",
        "ai"
    );


    const aiMessages =
        document.querySelectorAll(
            ".message.ai"
        );


    const aiMessage =
        aiMessages[
            aiMessages.length - 1
        ];


    const messageText =
        aiMessage.querySelector(
            ".message-text"
        );


    try {

        const response =
            await fetch(
                "/ask",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        question:
                            question

                    })

                }
            );


        const data =
            await response.json();


        if (data.success) {

            messageText.innerHTML =
                marked.parse(
                    data.answer || ""
                );

        } else {

            messageText.innerText =
                data.answer ||
                "Something went wrong.";

        }


    } catch (error) {

        console.error(
            "ASK ERROR:",
            error
        );


        messageText.innerText =
            "Something went wrong. Please try again.";

    }

}


// =====================================================
// ADD CHAT MESSAGE
// =====================================================

function addMessage(
    sender,
    text,
    type
) {

    const message =
        document.createElement(
            "div"
        );


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


    const strong =
        document.createElement(
            "strong"
        );


    strong.innerText =
        sender;


    const textDiv =
        document.createElement(
            "div"
        );


    textDiv.className =
        "message-text";


    textDiv.style.marginTop =
        "6px";


    textDiv.innerText =
        text;


    message.appendChild(
        strong
    );


    message.appendChild(
        textDiv
    );


    chatMessages.appendChild(
        message
    );


    chatMessages.scrollTop =
        chatMessages.scrollHeight;

}


// =====================================================
// SUMMARY
// =====================================================

// IMPORTANT:
// HTML calls showSummary()
function showSummary() {

    runTool(
        "/summary",
        "Generating your summary..."
    );

}


// Keep this too in case another button
// calls generateSummary()
function generateSummary() {

    showSummary();

}


// =====================================================
// 2-MARK
// =====================================================

function generateTwoMark() {

    runTool(
        "/two-mark",
        "Generating 2-mark questions..."
    );

}


// =====================================================
// 16-MARK
// =====================================================

function generateSixteenMark() {

    runTool(
        "/sixteen-mark",
        "Generating 16-mark questions..."
    );

}


// =====================================================
// IMPORTANT QUESTIONS
// =====================================================

function generateImportantQuestions() {

    runTool(
        "/important-questions",
        "Finding important questions..."
    );

}


// =====================================================
// TOOL HANDLER
// =====================================================

async function runTool(
    endpoint,
    loadingText
) {

    showLoading(
        loadingText
    );


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


        console.log(
            endpoint,
            data
        );


        if (data.success) {

            resultContent.innerHTML =
                marked.parse(
                    data.answer || ""
                );

        } else {

            resultContent.innerHTML = `
                <div class="tool-error">
                    ${escapeHtml(
                        data.answer ||
                        data.message ||
                        "Something went wrong."
                    )}
                </div>
            `;

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


// =====================================================
// LOADING
// =====================================================

function showLoading(
    message = "AI is thinking..."
) {

    resultCard.classList.remove(
        "hidden"
    );


    resultContent.innerHTML = `

        <div class="ai-thinking">

            <div class="ai-spinner"></div>

            <span>
                ${message}
            </span>

        </div>

    `;


    resultCard.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });

}


// =====================================================
// ENTER KEY
// =====================================================

if (questionInput) {

    questionInput.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter"
            ) {

                event.preventDefault();

                askQuestion();

            }

        }
    );

}


// =====================================================
// FOCUS QUESTION
// =====================================================

function focusQuestion() {

    if (!questionInput) {
        return;
    }


    questionInput.focus();


    questionInput.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });

}


// =====================================================
// CLOSE RESULT
// =====================================================

function closeResult() {

    resultCard.classList.add(
        "hidden"
    );

}


// =====================================================
// ESCAPE HTML
// =====================================================

function escapeHtml(text) {

    const div =
        document.createElement(
            "div"
        );


    div.innerText =
        text;


    return div.innerHTML;

}
