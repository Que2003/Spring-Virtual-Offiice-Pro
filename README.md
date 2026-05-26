# Spring Office

- Homepage: [Spring Office](https://que2003.github.io/Spring-Virtual-Offiice-Pro/)
- Working workspace: [Open the office](https://que2003.github.io/Spring-Virtual-Offiice-Pro/office.html)

Spring Office is a virtual workspace for teams to coordinate projects, schedules, follow-ups, and focused work. The homepage introduces the product and links into the interactive office.

## Works immediately in the browser

- Join and leave practical work areas: Front Desk, Project Workroom, Operations Desk, and Quiet Work.
- Update presence status so a team can see who is available, busy, or focusing.
- Turn meeting notes and updates into structured follow-ups.
- Run focus and break timers with saved work-time metrics.
- Open everyday tools such as Gmail, Calendar, Drive, Notion, Slack, and GitHub.
- Ask SpringBot for local help with work, schedules, focus time, and setup.

When no backend is connected, sample teammates are visibly labeled `Preview` rather than presented as real users.

## Enable shared online features

Deploy [Que2003/springbot-backend](https://github.com/Que2003/springbot-backend) as a Render web service. Then open **Setup** in Spring Office and enter its public URL.

With the backend connected:

- Current visitor presence and work-area membership synchronize for the team.
- Notes can use AI when `OPENAI_API_KEY` and `OPENAI_MODEL` are configured on the backend.
- SpringBot can use the same AI setup for assistance.

The Connected tools view provides honest outbound shortcuts. Connecting and reading account data will require secure OAuth integrations before it is offered as a feature.
