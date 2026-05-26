# Spring Office

- Homepage: [Spring Office](https://que2003.github.io/Spring-Virtual-Offiice-Pro/)
- Working workspace: [Open the office](https://que2003.github.io/Spring-Virtual-Offiice-Pro/office.html)

Spring Office is a virtual workspace for teams to coordinate projects, schedules, follow-ups, Discord communication, and focused work.

## Works immediately in the browser

- Choose Spring, Midnight, Blossom, Ocean, or Neon Black themes on the homepage and inside the office.
- Join and leave practical work areas: Front Desk, Project Workroom, Operations Desk, and Quiet Work.
- Update presence status so a team can see who is available, busy, or focusing.
- Turn meeting notes and updates into structured follow-ups.
- Run focus and break timers with saved work-time metrics.
- Open everyday tools such as Gmail, Calendar, Drive, Notion, Slack, and GitHub.
- Open the Discord Hub to see real SpringBot commands and Discord connection readiness.
- Use SpringBot's local planning templates for agendas, drafts, brainstorming prompts, and daily plans.

When no backend is connected, sample teammates are visibly labeled `Preview`, SpringBot reports `Local planning`, and Discord reports setup is needed rather than presenting a fake connection.

## Enable SpringBot, Discord, and shared online features

Deploy [Que2003/springbot-backend](https://github.com/Que2003/springbot-backend) as a Render web service, then enter its public URL in **Setup**.

With backend configuration enabled:

- Current visitor presence and work-area membership synchronize for the team.
- With `OPENAI_API_KEY` and `OPENAI_MODEL`, SpringBot can draft, brainstorm, plan, summarize, and answer open-ended work questions.
- With `DISCORD_TOKEN` and `DISCORD_APPLICATION_ID`, the Discord Hub verifies your existing bot and provides an Add to Discord action.
- With `DISCORD_CHANNEL_ID` and `OFFICE_ADMIN_KEY`, authorized users can post office updates into Discord as SpringBot.

Bot tokens remain on the backend and are never placed in the public website files.
