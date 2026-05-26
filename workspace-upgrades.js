(() => {
  const themeNames = ["spring", "midnight", "blossom", "ocean", "neon"];
  const themeLabels = { spring: "Spring", midnight: "Midnight", blossom: "Blossom", ocean: "Ocean", neon: "Neon Black" };
  const storageKey = "spring-office-theme";
  const history = { quickBotMessages: [], fullBotMessages: [] };
  const themePanel = document.createElement("section");
  themePanel.className = "workspace-themes";
  themePanel.innerHTML = `<span>Theme</span><div class="theme-swatches">${themeNames.map(theme => `<button class="theme-chip" data-theme="${theme}" type="button" title="${themeLabels[theme]}" aria-label="Use ${themeLabels[theme]} theme"><i></i></button>`).join("")}</div>`;
  document.querySelector(".brand").insertAdjacentElement("afterend", themePanel);

  function applyTheme(theme) {
    const next = themeNames.includes(theme) ? theme : "spring";
    document.documentElement.dataset.theme = next;
    localStorage.setItem(storageKey, next);
    document.querySelectorAll(".theme-chip").forEach(button => button.classList.toggle("active", button.dataset.theme === next));
  }
  themePanel.addEventListener("click", event => {
    const button = event.target.closest(".theme-chip");
    if (button) applyTheme(button.dataset.theme);
  });
  applyTheme(localStorage.getItem(storageKey) || "spring");

  const botViewSurface = document.querySelector("#view-bot .surface");
  const assistantState = document.createElement("div");
  assistantState.className = "assistant-state";
  assistantState.id = "assistantState";
  assistantState.innerHTML = "<strong>Local planning mode</strong>Connect your backend in Setup to activate full AI conversations.";
  botViewSurface.insertAdjacentElement("afterbegin", assistantState);
  const prompts = document.createElement("div");
  prompts.className = "assistant-prompts";
  prompts.innerHTML = ["Plan my day", "Draft a follow-up email", "Create a meeting agenda", "Brainstorm project ideas"].map(prompt => `<button type="button" data-prompt="${prompt}">${prompt}</button>`).join("");
  assistantState.insertAdjacentElement("afterend", prompts);

  function setAssistantMode(mode) {
    const label = el("botMode");
    if (mode === "ai") {
      label.textContent = "AI ready";
      assistantState.innerHTML = "<strong>AI ready</strong>SpringBot can draft, brainstorm, plan, summarize, and answer open-ended work questions.";
    } else if (mode === "connected") {
      label.textContent = "AI setup needed";
      assistantState.innerHTML = "<strong>Backend connected</strong>Add AI configuration on the backend to unlock intelligent, open-ended responses.";
    } else {
      label.textContent = "Local planning";
      assistantState.innerHTML = "<strong>Local planning mode</strong>Connect your backend in Setup to activate full AI conversations.";
    }
  }

  async function checkAssistantMode() {
    if (!state.apiUrl) { setAssistantMode("local"); return; }
    try {
      const response = await fetch(api("/health"));
      if (!response.ok) throw new Error();
      const data = await response.json();
      setAssistantMode(data.aiConfigured ? "ai" : "connected");
    } catch (_error) {
      setAssistantMode("local");
    }
  }

  function localPlanningReply(message) {
    const prompt = message.toLowerCase();
    if (prompt.includes("email") || prompt.includes("follow-up") || prompt.includes("follow up") || prompt.includes("draft")) {
      return "Draft template:\n\nSubject: Follow-up on [topic]\n\nHi [name],\nThanks for your time today. Here are the next steps we discussed: [next steps]. I will follow up by [date].\n\nBest,\n[Your name]\n\nConnect AI in Setup and I can turn your real context into a finished draft.";
    }
    if (prompt.includes("agenda") || prompt.includes("meeting")) {
      return "Meeting agenda:\n1. Goal and desired decision\n2. Current status and blockers\n3. Options to discuss\n4. Owners and next steps\n5. Due dates and follow-up\n\nConnect AI for an agenda tailored to your meeting details.";
    }
    if (prompt.includes("plan") || prompt.includes("day") || prompt.includes("priorit")) {
      return "A practical plan for today:\n1. List the one result that must be finished.\n2. Move active work into Project Workroom.\n3. Run a focus block on the highest-impact task.\n4. Record decisions and follow-ups in Project notes.\n5. Close with tomorrow's first action.\n\nAI mode can turn your actual task list into a prioritized plan.";
    }
    if (prompt.includes("brainstorm") || prompt.includes("idea")) {
      return "Start with three directions: improve an existing workflow, remove a repeated frustration, or test a small new offer. Share the goal and constraints in AI mode and SpringBot can develop specific ideas with tradeoffs.";
    }
    return "I can provide planning templates locally. For intelligent drafting, brainstorming, research-style questions, and conversation that understands context, connect an AI-enabled backend in Setup.";
  }

  function replaceThinking(containerId, node, text) {
    node.remove();
    addBubble(containerId, text, false);
  }

  sendChat = async function(message, containerId) {
    addBubble(containerId, message, true);
    history[containerId].push({ role: "user", content: message });
    if (!state.apiUrl) {
      const reply = localPlanningReply(message);
      history[containerId].push({ role: "assistant", content: reply });
      addBubble(containerId, reply, false);
      setAssistantMode("local");
      return;
    }
    const waiting = document.createElement("div");
    waiting.className = "bubble thinking";
    waiting.textContent = "SpringBot is thinking...";
    el(containerId).appendChild(waiting);
    try {
      const room = ROOMS.find(item => item.id === state.room)?.name || "No room selected";
      const response = await fetch(api("/api/chat"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, history: history[containerId].slice(-10), context: { room, status: state.me.status, name: state.me.name } })
      });
      if (!response.ok) throw new Error();
      const data = await response.json();
      const reply = data.reply || "I could not form a response right now.";
      history[containerId].push({ role: "assistant", content: reply });
      replaceThinking(containerId, waiting, reply);
      setAssistantMode(data.mode === "ai" ? "ai" : "connected");
    } catch (_error) {
      replaceThinking(containerId, waiting, localPlanningReply(message));
      notify("Assistant connection unavailable; using local planning mode.");
      setAssistantMode("local");
    }
  };

  prompts.addEventListener("click", event => {
    const button = event.target.closest("button[data-prompt]");
    if (!button) return;
    sendChat(button.dataset.prompt, "fullBotMessages");
  });
  el("settingsForm").addEventListener("submit", () => setTimeout(checkAssistantMode, 200));
  checkAssistantMode();
})();
