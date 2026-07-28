/* =========================================================
   VIDEO AGENT — FRONTEND LOGIC & RAG INTERACTION
   ========================================================= */

document.addEventListener('DOMContentLoaded', () => {
    const sourceInput = document.getElementById('sourceInput');
    const langSelect = document.getElementById('langSelect');
    const runBtn = document.getElementById('runBtn');
    
    const progressCard = document.getElementById('progressCard');
    const statusMsg = document.getElementById('statusMsg');
    const workspaceGrid = document.getElementById('workspaceGrid');

    const resTitle = document.getElementById('resTitle');
    const resSummary = document.getElementById('resSummary');
    const resDecisions = document.getElementById('resDecisions');
    const resQuestions = document.getElementById('resQuestions');
    const resActionItems = document.getElementById('resActionItems');
    const resTranscript = document.getElementById('resTranscript');
    const downloadBtn = document.getElementById('downloadBtn');

    const chatHistory = document.getElementById('chatHistory');
    const chatInput = document.getElementById('chatInput');
    const sendChatBtn = document.getElementById('sendChatBtn');

    let currentTranscriptText = "";

    // Step status helper
    function updateStep(stepIndex, msgText) {
        statusMsg.innerText = `⚡ ${msgText}`;
        for (let i = 0; i <= 5; i++) {
            const node = document.getElementById(`step-${i}`);
            if (!node) continue;
            node.classList.remove('active', 'done');
            if (i < stepIndex) {
                node.classList.add('done');
                node.querySelector('.node-circle').innerText = '✓';
            } else if (i === stepIndex) {
                node.classList.add('active');
                node.querySelector('.node-circle').innerText = i + 1;
            } else {
                node.querySelector('.node-circle').innerText = i + 1;
            }
        }
    }

    // Process Video Click Handler
    runBtn.addEventListener('click', async () => {
        const source = sourceInput.value.trim();
        const language = langSelect.value;

        if (!source) {
            alert('Please enter a YouTube URL or local audio file path!');
            return;
        }

        // Show loader, hide workspace
        progressCard.style.display = 'block';
        workspaceGrid.style.display = 'none';
        runBtn.disabled = true;
        runBtn.innerHTML = '<span>⏳ Processing...</span>';

        // Step simulation
        let stepIdx = 0;
        const stepMessages = [
            "Ingesting source video & converting audio...",
            "Transcribing audio with Whisper LLM...",
            "Generating executive title...",
            "Synthesizing detailed summary...",
            "Extracting action items, key decisions & questions...",
            "Building Chroma RAG vector store for instant chat..."
        ];

        updateStep(0, stepMessages[0]);
        const stepInterval = setInterval(() => {
            if (stepIdx < 4) {
                stepIdx++;
                updateStep(stepIdx, stepMessages[stepIdx]);
            }
        }, 3500);

        try {
            const response = await fetch('/api/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ source, language })
            });

            clearInterval(stepInterval);

            const result = await response.json();
            if (!response.ok || result.status !== 'success') {
                throw new Error(result.detail || 'Failed to process video.');
            }

            // Mark all steps done
            updateStep(6, "Processing complete! Insights ready.");

            const data = result.data;
            currentTranscriptText = data.transcript || "";

            // Render Results
            resTitle.innerText = data.title || "Video Analysis";
            resSummary.innerText = data.summary || "No summary generated.";

            // Render Decisions
            if (Array.isArray(data.key_decisions) && data.key_decisions.length > 0) {
                resDecisions.innerHTML = data.key_decisions
                    .map(d => `<span class="pill-tag cyan">🔑 ${d}</span>`)
                    .join('');
            } else {
                resDecisions.innerHTML = '<span class="pill-tag">None detected</span>';
            }

            // Render Questions
            if (Array.isArray(data.open_questions) && data.open_questions.length > 0) {
                resQuestions.innerHTML = data.open_questions
                    .map(q => `<span class="pill-tag pink">❓ ${q}</span>`)
                    .join('');
            } else {
                resQuestions.innerHTML = '<span class="pill-tag">None detected</span>';
            }

            // Render Action Items
            if (Array.isArray(data.action_items) && data.action_items.length > 0) {
                resActionItems.innerHTML = data.action_items
                    .map(item => `
                        <div class="task-item" onclick="this.classList.toggle('completed')">
                            <div class="task-check">✓</div>
                            <div style="font-size:0.95rem; color:var(--text-main);">${item}</div>
                        </div>
                    `).join('');
            } else {
                resActionItems.innerHTML = '<div style="color:var(--text-muted);">No action items found.</div>';
            }

            // Render Transcript
            resTranscript.innerText = currentTranscriptText;

            // Show Workspace
            setTimeout(() => {
                progressCard.style.display = 'none';
                workspaceGrid.style.display = 'grid';
                workspaceGrid.scrollIntoView({ behavior: 'smooth' });
            }, 600);

        } catch (err) {
            clearInterval(stepInterval);
            alert(`Error: ${err.message}`);
            progressCard.style.display = 'none';
        } finally {
            runBtn.disabled = false;
            runBtn.innerHTML = '<span>🚀 Process Video</span>';
        }
    });

    // Transcript Download Handler
    downloadBtn.addEventListener('click', () => {
        if (!currentTranscriptText) return;
        const blob = new Blob([currentTranscriptText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'transcript.txt';
        a.click();
        URL.revokeObjectURL(url);
    });

    // Chat Handler
    async function sendChatMessage() {
        const question = chatInput.value.trim();
        if (!question) return;

        // Append User Message
        const userMsgDiv = document.createElement('div');
        userMsgDiv.className = 'chat-msg user';
        userMsgDiv.innerText = question;
        chatHistory.appendChild(userMsgDiv);

        chatInput.value = '';
        chatHistory.scrollTop = chatHistory.scrollHeight;

        // Typing indicator
        const assistantMsgDiv = document.createElement('div');
        assistantMsgDiv.className = 'chat-msg assistant';
        assistantMsgDiv.innerText = '🤖 Searching video context vector store...';
        chatHistory.appendChild(assistantMsgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question })
            });

            const result = await response.json();
            if (!response.ok || result.status !== 'success') {
                throw new Error(result.detail || 'Could not answer question.');
            }

            assistantMsgDiv.innerText = `🤖 ${result.answer}`;
        } catch (err) {
            assistantMsgDiv.innerText = `⚠️ Error: ${err.message}`;
        }

        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    sendChatBtn.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') sendChatMessage();
    });

});
