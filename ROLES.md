# The six bots

Six is not a round number picked for a headline. It is the smallest set in which no role can both
make a decision and press the button that executes it.

**Read the right column first. That is the architecture. Everybody writes the left column first, and
it matters least.**

```
ROLE          OWNS                          STOPLINE
──────────────────────────────────────────────────────────────────────
TREASURER     wallet, runway, budgets       never earns anything
              the alive/dead verdict        and never spends on product

PROSPECTOR    demand discovery              never builds a product
              the hypothesis queue          and never talks to a customer

BUILDER       product, landing, deploy      never picks what to build
                                            and never sets the price

SELLER        price, thread, invoice        never touches the wallet,
                                            payments go to an address
                                            issued by TREASURER

REPLICATOR    spawning a child, mutation    never decides whether
                                            there is a surplus

REAPER        executing death, sweeping     lives outside the agent,
              residuals, the obituary       agent cannot switch it off
──────────────────────────────────────────────────────────────────────
```

Each role is a bot with its own persistent cloud computer, its own logins, its own memory. They hand
files to each other through a shared workspace.

## The flow

```
                   ┌──────────────┐
                   │  TREASURER   │  every 10 min: computes runway,
                   │   (wallet)   │  issues budget or declares death
                   └──────┬───────┘
                          │ cycle budget
             ┌────────────┼────────────┐
             ▼            ▼            ▼
      ┌────────────┐ ┌─────────┐ ┌──────────┐
      │ PROSPECTOR │→│ BUILDER │→│  SELLER  │
      │ who pays?  │ │  ship   │ │   sell   │
      └────────────┘ └─────────┘ └────┬─────┘
                                      │ revenue → wallet
                          ┌───────────┴──────────┐
                          ▼                      ▼
                    surplus?              runway < floor?
                          │                      │
                   ┌──────▼──────┐        ┌──────▼──────┐
                   │ REPLICATOR  │        │   REAPER    │
                   │ child + $5  │        │   death     │
                   └─────────────┘        └─────────────┘
```

## Why the stoplines matter more than the roles

A role without a stopline collapses into the role next to it. A seller who can touch the wallet stops
selling and starts spending. A prospector who can build stops looking for demand and starts building
what it finds interesting. A treasurer who can earn will forgive its own overspend.

The stopline is the only part of a role the model cannot talk itself out of, because it is enforced
by what credentials the bot holds — not by what its prompt says.

**The reaper is not a role in the population.** It runs outside, with credentials no agent holds, and
it is the one component that is never given a reason to be merciful.
