ROOMS.splice(0, ROOMS.length,
  { id: "brew", name: "Front Desk", description: "New inquiries, customer check-ins, and today's priorities" },
  { id: "engineering", name: "Client Workroom", description: "Active jobs, deliverables, and customer follow-ups" },
  { id: "design", name: "Operations Desk", description: "Scheduling, vendors, inventory, and admin" },
  { id: "focus", name: "Quiet Work", description: "Bookkeeping, proposals, and focused work" }
);
DEMO_PEOPLE.splice(0, DEMO_PEOPLE.length,
  { id: "demo-1", name: "Avery", status: "available", room: "engineering", activity: "Preparing a customer quote", demo: true },
  { id: "demo-2", name: "Jordan", status: "focus", room: "focus", activity: "Reconciling invoices", demo: true },
  { id: "demo-3", name: "Morgan", status: "busy", room: "design", activity: "Updating tomorrow's schedule", demo: true }
);
INTEGRATIONS.splice(0, INTEGRATIONS.length,
  { name: "QuickBooks", href: "https://quickbooks.intuit.com", detail: "Open accounting" },
  { name: "Square", href: "https://squareup.com/dashboard", detail: "Open payments" },
  { name: "Gmail", href: "https://mail.google.com", detail: "Open customer email" },
  { name: "Calendar", href: "https://calendar.google.com", detail: "Open schedule" },
  { name: "Google Drive", href: "https://drive.google.com", detail: "Open business files" },
  { name: "Shopify", href: "https://admin.shopify.com", detail: "Open orders" }
);
const businessViews={office:["Daily HQ","Keep your small team aligned on customers, jobs, and today's work."],notes:["Client and team notes","Turn calls and huddles into next steps."],wellness:["Focus time","Protect time for estimates, invoices, and follow-ups."],integrations:["Business tools","Open the services you already use to run the business."],bot:["SpringBot assistant","Get help organizing work and customer follow-ups."],settings:["Setup","Connect shared services and name your workspace."]};
setView=function(name){document.querySelectorAll(".view").forEach(view=>view.classList.toggle("active",view.id==="view-"+name));document.querySelectorAll(".nav button").forEach(button=>button.classList.toggle("active",button.dataset.view===name));el("viewTitle").textContent=businessViews[name][0];el("viewDescription").textContent=businessViews[name][1]};
localBotReply=function(message){const prompt=message.toLowerCase();if(prompt.includes("customer")||prompt.includes("client")||prompt.includes("follow"))return"Use Client and team notes to record the conversation and pull out follow-ups. Keep customer details out of shared rooms unless your team needs them.";if(prompt.includes("invoice")||prompt.includes("payment"))return"Open Business tools for QuickBooks or Square, and use Quiet Work for uninterrupted billing time.";if(prompt.includes("schedule")||prompt.includes("appointment"))return"Use Operations Desk to coordinate schedules, then open Calendar from Business tools.";if(prompt.includes("room"))return"Front Desk is for incoming work, Client Workroom is for active jobs, Operations Desk keeps the business moving, and Quiet Work protects focus time.";if(prompt.includes("connect")||prompt.includes("api"))return"Open Setup and enter your deployed backend URL so your team can share live room presence.";return"I can help organize customer follow-ups, schedules, invoices, focus time, or your shared workspace setup."};
document.querySelector(".brand small").textContent="Small business workspace";
document.querySelector(".rooms-label").textContent="Work areas";
document.querySelector('[data-view="office"]').innerHTML='<span class="icon">H</span>Daily HQ';
document.querySelector('[data-view="notes"]').innerHTML='<span class="icon">N</span>Client notes';
document.querySelector('[data-view="wellness"]').innerHTML='<span class="icon">T</span>Focus time';
document.querySelector('[data-view="integrations"]').innerHTML='<span class="icon">A</span>Business tools';
document.querySelector('[data-view="settings"]').innerHTML='<span class="icon">S</span>Setup';
document.querySelector("#view-notes h2").textContent="Client and team notes";
document.querySelector("#view-notes > p").textContent="Paste a customer call, staff huddle, or job update and capture clear follow-ups.";
document.querySelector("#view-notes h3").textContent="Call or huddle notes";
el("notesInput").placeholder="Example: Ms. Rivera approved the estimate. Que will send an invoice by Friday. Schedule installation for Tuesday.";
el("notesResult").textContent="Your recap and customer follow-ups appear here.";
document.querySelector("#view-wellness h2").textContent="Focus time";
document.querySelector("#view-wellness > p").textContent="Track protected time for estimates, billing, scheduling, and customer follow-ups.";
document.querySelector("#view-integrations h2").textContent="Business tools";
document.querySelector("#view-integrations > p").textContent="Open accounting, payments, email, scheduling, files, and orders in one place.";
document.querySelector("#view-integrations .integrations-note").textContent="These are real shortcuts to your services. Secure account syncing remains disabled until OAuth is configured.";
document.querySelector("#view-bot > p").textContent="Ask SpringBot for help with customer follow-ups, scheduling, billing focus blocks, or workspace setup.";
document.querySelector("#view-settings h2").textContent="Set up your workspace";
document.querySelector("#view-settings > p").textContent="Connect a backend URL when your team is ready for shared online rooms.";
document.querySelector('label[for="displayName"]').textContent="Your name";
document.querySelector('label[for="apiUrl"]').textContent="Shared office backend URL";
el("quickBotMessages").innerHTML="";el("fullBotMessages").innerHTML="";
addBubble("quickBotMessages","Hi. I can help organize today's customers, appointments, and follow-ups.",false);
addBubble("fullBotMessages","Ask about customer notes, schedules, invoice time, or team setup.",false);
state.events=["Start in Front Desk, or join Client Workroom for active customer work."];
renderOffice();renderIntegrations();setView("office");
