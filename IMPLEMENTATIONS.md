# Implementations of the Mortality Spec

A population conforms if it satisfies every **MUST** in [MORTALITY-SPEC.md](./MORTALITY-SPEC.md).
Framework, model and language are irrelevant. What matters is that the dying is real.

| Implementation | Stack | Mode | Agents spawned | Graveyard |
|---|---|---|---|---|
| **Automaton** (reference) | Grok Bot, 6 roles | live | see [GRAVEYARD.md](./GRAVEYARD.md) | [`/obituaries`](./obituaries) |

## Add yours

Open a PR with a row above and a link to your obituary corpus. To be listed as `live` rather than
`simulated`, the published figures must be reproducible from that corpus.

Checklist before you claim conformance:

- [ ] The reaper runs outside every agent, with credentials no agent holds
- [ ] Death is irreversible — no checkpoint, no restart, no operator override
- [ ] `death_floor` is the cost of one full working cycle, not zero
- [ ] The agent sees runway in hours, never a balance in dollars
- [ ] Time is billed, not only actions
- [ ] Every death writes an obituary conforming to the schema
- [ ] No role both decides and executes ([ROLES.md](./ROLES.md))
- [ ] Every denial in [DENIALS.md](./DENIALS.md) is enforced by a credential or an external check,
      not by a prompt
