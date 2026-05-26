# Spring Office for Small Businesses

- Homepage: [Spring Office](https://que2003.github.io/Spring-Virtual-Offiice-Pro/)
- Working workspace: [Open the office](https://que2003.github.io/Spring-Virtual-Offiice-Pro/office.html)

Spring Office is built for small teams that need a simple daily workspace for customers, schedules, follow-ups, and focused admin time. The homepage explains the product and links into the fully interactive office rather than replacing it.

## Works immediately in the browser

- Join and leave practical work areas: Front Desk, Client Workroom, Operations Desk, and Quiet Work.
- Update presence status so a small team can see who is available, busy, or focusing.
- Turn client calls, team huddles, and job updates into structured follow-ups.
- Run focus and break timers with saved work-time metrics.
- Open everyday business services such as QuickBooks, Square, Gmail, Calendar, Drive, and Shopify.
- Ask SpringBot for local help with customer work, appointments, invoice time, and setup.

When no backend is connected, sample teammates are visibly labeled `Preview` rather than presented as real users.

## Enable shared online features

Deploy [Que2003/springbot-backend](https://github.com/Que2003/springbot-backend) as a Render web service. Then open **Setup** in Spring Office and enter its public URL.

With the backend connected:

- Current visitor presence and work-area membership synchronize for the team.
- Notes can use AI when `OPENAI_API_KEY` and `OPENAI_MODEL` are configured on the backend.
- SpringBot can use the same AI setup for business assistance.

The current Business tools view provides honest outbound shortcuts. Connecting and reading QuickBooks, Square, Gmail, Calendar, Drive, or Shopify account data will require secure OAuth integrations before it is offered as a feature.
