async function refreshSources() {
  const res = await fetch("/sources");
  const sources = await res.json();

  const box = document.getElementById("sourceList");
  box.innerHTML = "";

  if (sources.length === 0) {
    box.innerHTML = "<p style='opacity:0.6'>No sources added</p>";
    return;
  }

  sources.forEach(s => {
    const div = document.createElement("div");
    div.innerHTML = `
      <span title="${s.value}">
        ${s.type.toUpperCase()}: ${s.value.split("/").pop()}
      </span>
      <button onclick="deleteSource('${encodeURIComponent(s.value)}')">🗑</button>
    `;
    box.appendChild(div);
  });
}

async function uploadPDF() {
  const fileInput = document.getElementById("pdfFile");
  const file = fileInput.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  await fetch("/ingest/pdf", { method: "POST", body: formData });
  fileInput.value = "";
  refreshSources();
}

async function uploadURL() {
  const input = document.getElementById("urlInput");
  const url = input.value.trim();
  if (!url) return;

  await fetch("/ingest/url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url })
  });

  input.value = "";
  refreshSources();
}

async function deleteSource(encodedValue) {
  await fetch(`/sources?value=${encodedValue}`, { method: "DELETE" });
  refreshSources();
}

function handleEnter(e) {
  if (e.key === "Enter") askQuestion();
}

async function askQuestion() {
  const input = document.getElementById("questionInput");
  const chatBox = document.getElementById("chatBox");
  const btn = document.getElementById("askBtn");

  const question = input.value.trim();
  if (!question) return;

  chatBox.innerHTML += `<div class="user-msg">${question}</div>`;
  input.value = "";
  btn.disabled = true;

  const thinking = document.createElement("div");
  thinking.className = "bot-msg";
  thinking.innerText = "Thinking...";
  chatBox.appendChild(thinking);
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    const data = await res.json();
    thinking.innerText = data.answer || "No response";
  } catch {
    thinking.innerText = "❌ Server error";
  }

  btn.disabled = false;
  chatBox.scrollTop = chatBox.scrollHeight;
}

refreshSources();
