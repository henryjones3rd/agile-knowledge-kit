---
title: Agile Delivery Knowledge Kit
description: Field-tested playbooks, decision guides, and templates for distributed engineering teams that want predictable delivery.
owner: Henry Jones III
last_reviewed: 2026-10-26
review_cycle_days: 180
tags: [overview]
---

# Agile Delivery Knowledge Kit

This kit turns delivery practices that usually live in a coach's head into
playbooks, decision guides, and templates any team can pick up on its own.

It is built for distributed teams: several time zones, several holiday
calendars, and a steady stream of requests from other teams.

## Start here

| If you want to... | Read |
| --- | --- |
| Join a new team without disrupting it | [Observe first](getting-started/observe-first.md) |
| Stop confusing story points with days | [Relative estimation](playbooks/relative-estimation.md) |
| Commit to work you can actually finish | [Capacity planning](playbooks/capacity-planning.md) |
| Get help from other teams without scrambling | [Feature Launch Reservations](playbooks/feature-launch-reservations.md) |
| Finish work instead of starting it | [Work in progress limits and swarming](playbooks/wip-limits-and-swarming.md) |
| Run a review stakeholders want to attend | [Sprint reviews](playbooks/sprint-reviews.md) |

## The problem this kit addresses

Teams in this situation often finish only about two thirds of what they commit
to each sprint, and most of that lands in the last two days. That end-of-sprint
spike is called the **hockey stick**.

The causes are usually structural, not personal:

1. Story points treated as days, so estimates become promises about hours.
2. Capacity differences across locations that nobody plans for.
3. Unplanned requests from other teams that never appear in the plan.

Each playbook targets one of those causes.

## How this site is built

Every page is Markdown in Git, checked in CI for broken links, stale content,
and terminology drift, then published automatically. An
[`llms.txt`](https://llmstxt.org/) file packages the content for AI assistants.
See [Contributing](contributing.md) for the full workflow.
