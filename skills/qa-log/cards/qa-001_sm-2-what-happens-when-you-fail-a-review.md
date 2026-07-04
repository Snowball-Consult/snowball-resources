---
id: qa-001
created: 2026-07-04
source: terminal
tags: spaced-repetition
type: recall
interval: 0
ease: 2.50
reps: 0
next_review: 2026-07-04
last_reviewed:
last_grade:
---

## Question

In SM-2 spaced repetition, what happens to a card's interval and ease factor when you fail a review?

## Answer

The interval resets to 1 day, the ease factor drops by 0.20 (with a floor of 1.30), and the consecutive-successful-reps counter resets to 0. The card then climbs the ladder again: 1 day, 3 days, then interval times ease.

**Why it matters:** Failing a card is cheap by design - the algorithm simply brings it back sooner, and the lowered ease keeps future intervals shorter until you prove you know it.

## Review history

| Date | Grade | Interval (d) | Next review |
|------|-------|--------------|-------------|
