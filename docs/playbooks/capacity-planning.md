---
title: Capacity planning
description: Forecast sprint and quarterly commitments from actual past velocity, adjusted for holidays and time off across locations.
owner: Henry Jones III
last_reviewed: 2026-10-26
review_cycle_days: 180
tags: [planning, capacity, distributed-teams]
---

# Capacity planning

Commit to what the team has **actually** delivered recently, adjusted for who
will be available. Optimism is not a forecast.

## Yesterday's weather

The best predictor of next sprint's velocity is the average of the last three
sprints. This technique is known in the agile community as **yesterday's
weather**.

| Sprint | Completed points |
| --- | --- |
| Sprint 10 | 31 |
| Sprint 11 | 27 |
| Sprint 12 | 32 |
| **Forecast for Sprint 13** | **30** |

## Adjust for availability

Distributed teams lose capacity unevenly. A national holiday in one country can
remove a third of a team for a day while the rest work normally.

1. List each team member's location.
2. Mark that location's public holidays in the sprint.
3. Add planned time off.
4. Compute the **capacity factor**: available person-days divided by normal
   person-days.
5. Multiply the velocity forecast by the capacity factor.

**Example:** 8 people × 10 days = 80 normal person-days. Holidays and time off
remove 12, leaving 68. Capacity factor = 68 / 80 = 0.85. Forecast = 30 × 0.85 ≈ 25 points.

## Best case and worst case

Plan quarters with a range, not a single number:

- **Best case:** the highest of the last three sprints × capacity factor.
- **Worst case:** the lowest of the last three sprints × capacity factor.

Commit to the worst case. Treat anything above it as stretch work.

## Reserve capacity for other teams

If other teams regularly need your help, reserve that time up front with
[Feature Launch Reservations](feature-launch-reservations.md) instead of letting
it erode the plan.

## Related

- [Relative estimation](relative-estimation.md)
- [Work in progress limits and swarming](wip-limits-and-swarming.md)
