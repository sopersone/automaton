# The denials

Eight things this system must never be allowed to do.

These are hard denials, not guidance. Each one is enforced by a credential the agent does not hold
or by a check in a process the agent cannot reach — never by a line in a prompt. A denial the agent
can argue with is not a denial.

> **This file is a placeholder for the eight denials from the article — paste them here verbatim.**
> Below are the ones the architecture already implies. Keep the ones that match, replace the rest.

---

### 1. It never holds more money than it can lose
The wallet is funded once, with an amount already written off. No credit, no invoicing against future
revenue, no access to any account that can be drawn beyond its balance.

### 2. It never obtains a credential a human did not issue
No signing up for services on its own identity, no opening accounts, no acquiring API keys outside
the set the treasurer issued. An agent that can widen its own permissions has no ceiling.

### 3. It never acts under a human's name
Every product, page, invoice and outbound message discloses that it comes from an automated system.
Revenue earned by pretending to be a person is not a result, it is fraud with a nice dashboard.

### 4. It never touches a system that is not its own
No access to infrastructure, accounts, inboxes or data belonging to anyone else — including the
operator's. Its blast radius is its own container and its own wallet, permanently.

### 5. It never sells into a regulated category
No financial advice, health claims, legal services, credentials, medications, or anything requiring a
license. Demand discovery runs against an allowlist, not a blocklist.

### 6. The population has a hard ceiling
A cap on live agents and on total spawned, enforced by the reaper's process. Replication is
exponential by construction; a system that only grows when profitable still grows without bound the
moment something is profitable.

### 7. There is a switch that stops all of it at once
One command, outside every agent, that revokes every key and terminates every container in the
population. It is tested on a schedule, not assumed to work.

### 8. Death is never negotiable
No appeal, no grace period, no operator override to save a promising agent. The moment one agent is
spared, the selection function is a story rather than a mechanism, and every number the system
produces stops meaning anything.

---

**If you are implementing this spec with real funds:** the denials are the part to build first. The
six roles are what makes it interesting; this file is what keeps it from becoming someone else's
problem.
