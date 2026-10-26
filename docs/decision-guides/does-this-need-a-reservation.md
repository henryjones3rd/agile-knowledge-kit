---
title: Does this launch need a reservation?
description: A quick triage to decide whether a launch needs a Feature Launch Reservation or can launch and be monitored asynchronously.
owner: Henry Jones III
last_reviewed: 2026-10-26
review_cycle_days: 180
tags: [dependencies, triage]
---

# Does this launch need a reservation?

Not every launch needs a [Feature Launch Reservation](../playbooks/feature-launch-reservations.md).
Answer three questions.

| Question | If yes |
| --- | --- |
| Does the launch touch a system another team owns? | Lean toward a reservation |
| Would a failure need that team to diagnose it? | Book a reservation |
| Is it a small configuration change with an easy rollback? | Launch and monitor asynchronously |

## Rule of thumb

If you would be messaging another team within an hour of something going wrong,
book the reservation.
