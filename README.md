# Spring Virtual Office Pro

The main page is now the working office application at [GitHub Pages](https://que2003.github.io/Spring-Virtual-Offiice-Pro/).

## Works immediately in the browser

- Join and leave smart rooms and update your presence status.
- Run focus and break timers with saved wellness metrics.
- Produce local structured meeting recaps from notes.
- Open configured workspace-tool shortcuts.
- Ask SpringBot for local navigation and setup help.

When no backend is connected, sample teammates are visibly labeled `Preview` rather than presented as real users.

## Enable shared online features

Deploy [Que2003/springbot-backend](https://github.com/Que2003/springbot-backend) as a Render web service. Then open **Settings** in the office and enter its public URL.

With the backend connected:

- Presence and room membership synchronize for current visitors.
- Meeting notes can use AI when `OPENAI_API_KEY` and `OPENAI_MODEL` are configured on the backend.
- SpringBot can use the same backend AI configuration.

External Slack, Notion, Jira, GitHub, Calendar, and Zoom account syncing is intentionally not claimed until OAuth credentials and callback flows are implemented. The current interface provides honest outbound tool shortcuts.
