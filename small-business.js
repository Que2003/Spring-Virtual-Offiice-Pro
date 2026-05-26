ROOMS.splice(0, ROOMS.length,
  { id: "brew", name: "Front Desk", description: "New requests, check-ins, and today's priorities" },
  { id: "engineering", name: "Project Workroom", description: "Active projects, deliverables, and follow-ups" },
  { id: "design", name: "Operations Desk", description: "Scheduling, coordination, files, and admin" },
  { id: "focus", name: "Quiet Work", description: "Planning, writing, and focused work" }
);
DEMO_PEOPLE.splice(0, DEMO_PEOPLE.length,
  { id: "demo-1", name: "Avery", status: "available", room: "engineering", activity: "Preparing a project update", demo: true },
  { id: "demo-2", name: "Jordan", status: "focus", room: "focus", activity: "Finishing a draft", demo: true },
  { id: "demo-3", name: "Morgan", status: "busy", room: "design", activity: "Updating tomorrow's schedule", demo: true }
);
INTEGRATIONS.splice(0, INTEGRATIONS.length,
  { name: "Gmail", href: "https://mail.google.com", detail: "Open email" },
  { name: "Calendar", href: "https://calendar.google.com", detail: "Open schedule" },
  { name: "Google Drive", href: "https://drive.google.com", detail: "Open files" },
  { name: "Notion", href: "https://www.notion.so", detail: "Open notes" },
  { name: "Slack", href: "https://slack.com", detail: "Open messages" },
  { name: "GitHub", href: "https://github.com", detail: "Open projects" }
);
const businessViews={office:["Daily HQ","Keep your team aligned on projects, priorities, and today's work."],notes:["Project and team notes","Turn meetings and updates into next steps."],wellness:["Focus time","Protect time for planning, writing, scheduling, and follow-ups."],integrations:["Connected tools","Open the services your team uses in one view."],bot:["SpringBot assistant","Get help organizing work and follow-ups."],settings:["Setup","Connect shared services and name your workspace."]};
setView=function(name){document.querySelectorAll(".view").forEach(view=>view.classList.toggle("active",view.id==="view-"+name));document.querySelectorAll(".nav button").forEach(button=>button.classList.toggle("active",button.dataset.view===name));el("viewTitle").textContent=businessViews[name][0];el("viewDescription").textContent=businessViews[name][1]};
localBotReply=function(message){const prompt=message.toLowerCase();if(prompt.includes("project")||prompt.includes("note")||prompt.includes("follow"))return"Use Project and team notes to record the discussion and pull out follow-ups. Keep sensitive details limited to the people who need them.";if(prompt.includes("write")||prompt.includes("draft"))return"Use Quiet Work for uninterrupted drafting time, then record next steps in Project notes.";if(prompt.includes("schedule")||prompt.includes("appointment"))return"Use Operations Desk to coordinate schedules, then open Calendar from Connected tools.";if(prompt.includes("room"))return"Front Desk is for incoming work, Project Workroom is for active projects, Operations Desk handles coordination, and Quiet Work protects focus time.";if(prompt.includes("connect")||prompt.includes("api"))return"Open Setup and enter your deployed backend URL so your team can share live room presence.";return"I can help organize follow-ups, schedules, focus time, or your shared workspace setup."};
document.querySelector(".brand small").textContent="Virtual workspace";
document.querySelector(".rooms-label").textContent="Work areas";
document.querySelector('[data-view="office"]').innerHTML='<span class="icon">H</span>Daily HQ';
document.querySelector('[data-view="notes"]').innerHTML='<span class="icon">N</span>Project notes';
document.querySelector('[data-view="wellness"]').innerHTML='<span class="icon">T</span>Focus time';
document.querySelector('[data-view="integrations"]').innerHTML='<span class="icon">A</span>Connected tools';
document.querySelector('[data-view="settings"]').innerHTML='<span class="icon">S</span>Setup';
document.querySelector("#view-notes h2").textContent="Project and team notes";
document.querySelector("#view-notes > p").textContent="Paste meeting notes or an update and capture clear follow-ups.";
document.querySelector("#view-notes h3").textContent="Meeting notes";
el("notesInput").placeholder="Example: The team approved the plan. Que will share the draft by Friday. Schedule the review for Tuesday.";
el("notesResult").textContent="Your recap and follow-ups appear here.";
document.querySelector("#view-wellness h2").textContent="Focus time";
document.querySelector("#view-wellness > p").textContent="Track protected time for planning, writing, scheduling, and follow-ups.";
document.querySelector("#view-integrations h2").textContent="Connected tools";
document.querySelector("#view-integrations > p").textContent="Open email, scheduling, files, and the services your team uses.";
document.querySelector("#view-integrations .integrations-note").textContent="These are real shortcuts to your services. Secure account syncing remains disabled until OAuth is configured.";
document.querySelector("#view-bot > p").textContent="Ask SpringBot for help with follow-ups, scheduling, focus blocks, or workspace setup.";
document.querySelector("#view-settings h2").textContent="Set up your workspace";
document.querySelector("#view-settings > p").textContent="Connect a backend URL when your team is ready for shared online rooms.";
document.querySelector('label[for="displayName"]').textContent="Your name";
document.querySelector('label[for="apiUrl"]').textContent="Shared office backend URL";
el("quickBotMessages").innerHTML="";el("fullBotMessages").innerHTML="";
addBubble("quickBotMessages","Hi. I can help organize today's work, schedules, and follow-ups.",false);
addBubble("fullBotMessages","Ask about project notes, schedules, focus time, or team setup.",false);
state.events=["Start in Front Desk, or join Project Workroom for active work."];
renderOffice();renderIntegrations();setView("office");
