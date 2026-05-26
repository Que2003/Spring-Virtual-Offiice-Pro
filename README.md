# Spring Office

- Homepage: [Spring Office](https://que2003.github.io/Spring-Virtual-Offiice-Pro/)
- Working workspace: [Open the office](https://que2003.github.io/Spring-Virtual-Offiice-Pro/office.html)

Spring Office is a virtual workspace for teams to coordinate projects, schedules, follow-ups, and focused work. The homepage introduces the product and links into the interactive office.

## Works immediately in the browser

- Choose Spring, Midnight, Blossom, Ocean, or Neon Black themes on the homepage and inside the office.
- Join and leave practical work areas: Front Desk, Project Workroom, Operations Desk, and Quiet Work.
- Update presence status so a team can see who is available, busy, or focusing.
- Turn meeting notes and updates into structured follow-ups.
- Run focus and break timers with saved work-time metrics.
- Open everyday tools such as Gmail, Calendar, Drive, Notion, Slack, and GitHub.
- Use SpringBot's local planning templates for agendas, drafts, brainstorming prompts, and daily plans.

When no backend is connected, sample teammates are visibly labeled `Preview` and SpringBot reports `Local planning` rather than pretending to be a full AI assistant.

## Enable intelligent SpringBot and shared online features

Deploy [Que2003/springbot-backend](https://github.com/Que2003/springbot-backend) as a Render web service. Configure `OPENAI_API_KEY` and `OPENAI_MODEL` on that backend, then open **Setup** in Spring Office and enter its public URL.

With an AI-enabled backend connected:

- Current visitor presence and work-area membership synchronize for the team.
- Notes can generate AI-assisted summaries and action items.
- SpringBot switches to `AI ready`, remembers recent conversation turns, receives active workspace context, and can draft, brainstorm, plan, summarize, and answer open-ended work questions.

The Connected tools view provides honest outbound shortcuts. Connecting and reading account data will require secure OAuth integrations before it is offered as a feature.
