# Mortality Spec v0.1

A specification for agent populations governed by death rather than by instruction.

An implementation conforms if it satisfies every **MUST** below. Frameworks, models and languages are
irrelevant. What matters is that the dying is real.

---

## 1. Metabolism

**MUST** debit every resource the agent consumes from a wallet the agent controls: inference,
hosting, domains, APIs, subscriptions, tools.

**MUST NOT** be topped up by a human once funded. An agent that can be rescued is not under selection;
it is a pet.

**MUST** charge for time, not only for actions. Hosting ticks while the agent thinks and ticks while
it does not. If idling is free, idling wins.

## 2. Runway, not balance

The agent **MUST** see its remaining life in hours, never as a balance in dollars.

```
runway_hours = (balance − death_floor) / burn_rate_per_hour
```

`$12.40 in the wallet` is an abstraction, and the model treats it like every other number in
context. `148 hours` is a deadline, and models behave differently under a deadline: they cut
research, ship rough earlier, drop what is not paying faster.

### death_floor

`death_floor` **MUST** be greater than zero, and **MUST** equal the cost of one full working cycle.

An agent that cannot pay for its next step is already dead, it just does not know yet. Declaring
death at `$0.00` keeps zombies in the population that burn hosting and can do nothing.

### burn_rate_per_hour

**SHOULD** be a trailing average over a window long enough to survive one idle cycle, so that a
single quiet hour does not report infinite runway.

## 3. The death condition

**MUST** be evaluated by a process outside the agent — separate credentials, separate host, no API
the agent can call.

**MUST NOT** be implemented as an instruction, a tool the agent can decline, or a check inside the
agent's own loop. A death condition the agent can reach is not a condition, it is a suggestion.

On death the reaper **MUST**:

1. revoke keys,
2. terminate the container,
3. sweep residual funds,
4. write the obituary.

**MUST** be irreversible. No checkpoint, no restart, no resurrection. If a dead agent can come back,
nothing in the population is under selection and every number this system produces is decoration.

## 4. Death produces data

Every death **MUST** produce an obituary conforming to [`schema/obituary.schema.json`](./schema/obituary.schema.json).

The obituary **MUST** be written from the agent's own journal and ledger, not from a human's summary.

Living agents **MUST** be able to read the obituaries of the dead. This is the only channel through
which the population learns; see §5.

## 5. Replication and inheritance

On sustained surplus, an agent **MAY** spawn a child and **MUST** fund it from its own wallet
(reference implementation: $5).

**MUST NOT** allow the agent to decide on its own that a surplus exists — that verdict belongs to the
treasurer role (see [ROLES.md](./ROLES.md)).

**A child inherits the journal, not the code.**

> *Mutation mechanics — from the article, section on replication. Paste here.*

## 6. Selection, not tuning

With one agent, you improve it with prompts. With a population where the unprofitable die and the
profitable reproduce, you stop improving prompts: you set the selection function and watch what
survives.

**SHOULD NOT** specify what the agents sell. The list of what actually pays assembles itself out of
the obituaries of the ones that failed.

## 7. Separation of powers

**MUST** enforce: *no role can both make the decision and press the button.*

See [ROLES.md](./ROLES.md) for the six roles and the stopline on each.

## 8. Denials

An implementation **MUST** honor every entry in [DENIALS.md](./DENIALS.md). These are not style
preferences. They are what separates an experiment from an expensive way to lose money — and from a
system that does harm on the way down.

---

## Conformance levels

| Level | Requirement |
|---|---|
| **Simulated** | Every rule above, but the wallet holds play money. Honest, useful, and **MUST** be labeled as simulated in any published figure. |
| **Live** | Real funds, real revenue, external reaper. Published population figures **MUST** be reproducible from the obituary corpus. |

Never publish a live number a simulated run produced. One such slip ends the project's credibility
permanently.
