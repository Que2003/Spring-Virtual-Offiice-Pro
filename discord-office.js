(() => {
  const workspace = document.querySelector('.workspace');
  const setupButton = document.querySelector('.nav button[data-view="settings"]');
  const discordButton = document.createElement('button');
  discordButton.type = 'button';
  discordButton.dataset.view = 'discord';
  discordButton.innerHTML = '<span class="icon">D</span>Discord';
  setupButton.insertAdjacentElement('beforebegin', discordButton);

  const view = document.createElement('div');
  view.className = 'view content-view';
  view.id = 'view-discord';
  view.innerHTML = `
    <h2>Discord Hub</h2>
    <p>Bring SpringBot into your Discord server and keep the office connected to your team conversations.</p>
    <div class="discord-grid">
      <section class="discord-card">
        <h3>SpringBot connection</h3>
        <p>The bot token stays on your backend. This page only checks readiness and opens the safe Discord install flow.</p>
        <div class="discord-status">
          <div><strong id="discordBotName">SpringBot</strong><small id="discordDetail">Connect your backend in Setup to check Discord.</small></div>
          <span class="discord-badge" id="discordBadge">Not connected</span>
        </div>
        <div class="discord-actions">
          <a class="button disabled" id="discordInvite" href="#" target="_blank" rel="noopener">Add to Discord</a>
          <button class="button secondary" type="button" id="discordRefresh">Check status</button>
        </div>
        <div class="discord-callout"><strong>Already in Discord?</strong> Use <code>!help</code> in your server to see every SpringBot command.</div>
      </section>
      <section class="discord-card">
        <h3>Useful commands</h3>
        <p>These commands are already implemented by your Discord bot.</p>
        <div class="command-list">
          <div class="command"><code>!help</code><span>Full command menu</span></div>
          <div class="command"><code>!play &lt;song&gt;</code><span>Play music in voice</span></div>
          <div class="command"><code>!spotify login</code><span>Link Spotify playback</span></div>
          <div class="command"><code>!rewrite tone | text</code><span>Writing assistance</span></div>
          <div class="command"><code>!poll question | options</code><span>Team decisions</span></div>
        </div>
      </section>
      <section class="discord-card">
        <h3>Post an office update</h3>
        <p>Send an announcement to your configured Discord channel as SpringBot.</p>
        <form class="discord-form" id="discordMessageForm">
          <label for="discordMessage">Announcement</label>
          <textarea id="discordMessage" placeholder="Project Workroom is open for today's planning session." maxlength="1800"></textarea>
          <label for="discordAdminKey">Admin posting key</label>
          <input class="field" id="discordAdminKey" type="password" autocomplete="off" placeholder="Required to send to Discord">
          <button class="button" type="submit">Send with SpringBot</button>
        </form>
        <p class="discord-feedback" id="discordFeedback"></p>
      </section>
      <section class="discord-card">
        <h3>Setup required</h3>
        <p>In your backend host, set the bot token, Discord application ID, destination channel ID, and an admin posting key. Then save that backend URL in Office Setup.</p>
        <div class="command-list">
          <div class="command"><code>DISCORD_TOKEN</code><span>Bot authentication</span></div>
          <div class="command"><code>DISCORD_APPLICATION_ID</code><span>Add-to-server link</span></div>
          <div class="command"><code>DISCORD_CHANNEL_ID</code><span>Update destination</span></div>
          <div class="command"><code>OFFICE_ADMIN_KEY</code><span>Protect posting</span></div>
        </div>
      </section>
    </div>`;
  workspace.appendChild(view);

  const priorSetView = setView;
  setView = function(name) {
    if (name !== 'discord') {
      priorSetView(name);
      discordButton.classList.remove('active');
      return;
    }
    document.querySelectorAll('.view').forEach(item => item.classList.toggle('active', item.id === 'view-discord'));
    document.querySelectorAll('.nav button').forEach(button => button.classList.toggle('active', button.dataset.view === 'discord'));
    el('viewTitle').textContent = 'Discord Hub';
    el('viewDescription').textContent = 'Connect SpringBot to your Discord server and share office updates.';
    loadDiscordStatus();
  };
  discordButton.addEventListener('click', () => setView('discord'));

  function setStatus(label, detail, ready, inviteUrl, canPost) {
    el('discordBotName').textContent = label || 'SpringBot';
    el('discordDetail').textContent = detail;
    el('discordBadge').textContent = ready ? 'Ready' : 'Setup needed';
    el('discordBadge').classList.toggle('ready', ready);
    const invite = el('discordInvite');
    invite.href = inviteUrl || '#';
    invite.classList.toggle('disabled', !inviteUrl);
    const sendButton = document.querySelector('#discordMessageForm button[type="submit"]');
    sendButton.disabled = !canPost;
  }

  async function loadDiscordStatus() {
    if (!state.apiUrl) {
      setStatus('SpringBot', 'Connect your backend in Setup to check Discord.', false, '', false);
      return;
    }
    el('discordDetail').textContent = 'Checking Discord configuration...';
    try {
      const response = await fetch(api('/api/discord/status'));
      if (!response.ok) throw new Error();
      const data = await response.json();
      const detail = data.botConnected ? 'Bot verified with Discord and ready for your server.' : data.configured ? 'Bot credentials are saved; Discord verification is pending.' : 'Add Discord settings on your backend to connect SpringBot.';
      setStatus(data.botName || 'SpringBot', detail, Boolean(data.botConnected), data.inviteUrl, Boolean(data.canPost));
    } catch (_error) {
      setStatus('SpringBot', 'Discord bridge is unavailable on this backend.', false, '', false);
    }
  }

  el('discordRefresh').addEventListener('click', loadDiscordStatus);
  el('discordMessageForm').addEventListener('submit', async event => {
    event.preventDefault();
    const text = el('discordMessage').value.trim();
    const adminKey = el('discordAdminKey').value;
    if (!state.apiUrl) { el('discordFeedback').textContent = 'Connect the backend in Setup first.'; return; }
    if (!text || !adminKey) { el('discordFeedback').textContent = 'Enter an announcement and the admin posting key.'; return; }
    el('discordFeedback').textContent = 'Sending through SpringBot...';
    try {
      const response = await fetch(api('/api/discord/message'), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: text, adminKey }) });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Unable to send message.');
      el('discordFeedback').textContent = 'Announcement posted to Discord.';
      el('discordMessage').value = '';
      el('discordAdminKey').value = '';
    } catch (error) {
      el('discordFeedback').textContent = error.message || 'Unable to send message.';
    }
  });
})();
