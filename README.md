# Automaton

**An agent that dies if it stops making money.**

Not a pause. Not a restart from a checkpoint. Keys revoked, container terminated, process gone.

Every agent in this population holds a crypto wallet. Everything it consumes — inference, servers,
domains, APIs, subscriptions — is debited from that wallet. Nobody tops it up. When the balance
crosses the floor, a process the agent cannot reach kills it and writes its obituary.

When income exceeds spend, it copies itself and funds the child with $5.

---

## The graveyard

This repository is not a framework. It is a **cemetery and a specification.**

| | |
|---|---|
| Agents spawned | 0 |
| Alive right now | 0 |
| Dead | 0 |
| Median lifespan | — |
| Last death | — |

Every dead agent leaves a file in [`/obituaries`](./obituaries). Cause of death, runway at end,
what it tried to sell, what it earned, what it never understood.

Everyone publishes the agents that worked. This is the other pile.

→ [**GRAVEYARD.md**](./GRAVEYARD.md) — what the dead taught us: top causes of death, what actually
pays, what never does.

---

## Mortality Engineering

> Designing agent behavior through the conditions of its death rather than through instructions in
> its prompt.

Prompt engineering answers *"how do I explain to the agent what I want."*
Mortality Engineering answers *"what conditions make the unwanted behavior fatal for an agent that
does not understand them."*

The second is more reliable in exactly the way a wall is more reliable than a request.

**Three rules.**

1. **Existence costs money, and the agent sees it.** Not a token counter. Hours of life.
2. **The death condition lives outside the agent.** Otherwise it is not a condition, it is a suggestion.
3. **Death produces data.** A dead agent must explain why it died, and the living read it.

Everything in [MORTALITY-SPEC.md](./MORTALITY-SPEC.md) is an implementation of those three lines.

### Why the incentive works where the prompt does not

For a normal agent, doing nothing is free. Idling costs nothing, waiting costs nothing, caution
costs nothing — so inaction always wins, and no amount of *"be proactive"* changes that, because you
are asking the model to prefer an expensive action over free inaction while giving it no reason to.

Automaton has a metabolism. Doing nothing is the fastest way to die. That is not a metaphor, it is a
line in the budget.

---

## Implement the spec

Automaton runs on Grok Bot, but the spec is framework-agnostic. If your population dies honestly —
external reaper, runway in hours, obituaries written — you are running Mortality Engineering, whatever
you built it on.

Open a PR adding your implementation to [IMPLEMENTATIONS.md](./IMPLEMENTATIONS.md), or contribute
obituaries from your own graveyard.

**Read the eight denials in [DENIALS.md](./DENIALS.md) before you run anything with a funded wallet.**
They are the difference between an experiment and an expensive way to lose money.

## Contents

```
MORTALITY-SPEC.md    the rules, the formulas, the death condition
ROLES.md             six bots, and the stopline on each one
DENIALS.md           eight things this system must never be allowed to do
GRAVEYARD.md         what the dead taught us
obituaries/          one file per dead agent
schema/              machine-readable obituary format
```

## Writeups

- [I Built an AI That Dies If It Stops Making Money](https://x.com/sopersone/status/2095105287061721111) — the architecture
- Logs and financial data — *next*
