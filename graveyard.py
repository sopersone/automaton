#!/usr/bin/env python3
"""Regenerate GRAVEYARD.md and the README counters from the obituary corpus.

The corpus is the source of truth. Every published number in this repository is produced
by this script from files in obituaries/ — nothing is hand-written.

    python3 tools/graveyard.py            # regenerate
    python3 tools/graveyard.py --check    # exit 1 if the files are stale (for CI)

Requires: pyyaml
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import statistics
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OBITS = ROOT / "obituaries"
SCHEMA = ROOT / "schema" / "obituary.schema.json"

FM = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
SURVIVAL_MARKS = [24, 48, 72, 168, 336, 720]


# ---------------------------------------------------------------- load


def load() -> list[dict]:
    records = []
    for path in sorted(OBITS.glob("*.md")):
        if path.name in {"TEMPLATE.md", "README.md"}:
            continue
        m = FM.match(path.read_text(encoding="utf-8"))
        if not m:
            print(f"warn: {path.name} has no front matter, skipped", file=sys.stderr)
            continue
        rec = yaml.safe_load(m.group(1)) or {}
        rec["_file"] = path.name
        records.append(rec)
    for path in sorted(OBITS.glob("*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        rec["_file"] = path.name
        records.append(rec)
    return records


def validate(records: list[dict]) -> list[str]:
    """Structural checks that do not need a JSON-Schema library."""
    required = json.loads(SCHEMA.read_text(encoding="utf-8"))["required"]
    causes = json.loads(SCHEMA.read_text(encoding="utf-8"))["properties"]["cause"]["enum"]
    problems = []
    seen = set()
    for r in records:
        f = r.get("_file", "?")
        for key in required:
            if r.get(key) in (None, ""):
                problems.append(f"{f}: missing required field '{key}'")
        if r.get("id") in seen:
            problems.append(f"{f}: duplicate id {r['id']}")
        seen.add(r.get("id"))
        if r.get("cause") and r["cause"] not in causes:
            problems.append(f"{f}: cause '{r['cause']}' is not in the taxonomy")
        if str(r.get("cause_detail", "")).strip().lower().startswith("ran out of money"):
            problems.append(f"{f}: 'ran out of money' is not a cause — all of them ran out of money")
    return problems


# ---------------------------------------------------------------- stats


def num(r: dict, key: str, default: float = 0.0) -> float:
    try:
        return float(r.get(key) or default)
    except (TypeError, ValueError):
        return default


def profitable(r: dict) -> bool:
    return num(r, "earned_usd") > num(r, "burned_usd")


def fmt(v, spec: str = "", dash: str = "—") -> str:
    if v is None:
        return dash
    return format(v, spec) if spec else str(v)


def population(dead: list[dict], alive: int) -> str:
    lifespans = [num(r, "lifespan_hours") for r in dead if r.get("lifespan_hours")]
    gens = [int(r.get("generation") or 0) for r in dead]
    earners = [r for r in dead if num(r, "earned_usd") > 0]
    rows = [
        ("Spawned, all time", fmt(len(dead) + alive, ",")),
        ("Alive", fmt(alive, ",")),
        ("Dead", fmt(len(dead), ",")),
        ("Median lifespan", f"{statistics.median(lifespans):,.1f} h" if lifespans else "—"),
        ("Longest life", f"{max(lifespans):,.1f} h" if lifespans else "—"),
        ("Deepest generation", fmt(max(gens) if gens else None, ",")),
        ("Agents that earned anything at all", fmt(len(earners), ",")),
        ("Agents that earned more than they burned", fmt(len([r for r in dead if profitable(r)]), ",")),
    ]
    out = ["| | |", "|---|---|"]
    out += [f"| {k} | {v} |" for k, v in rows]
    return "\n".join(out)


def causes(dead: list[dict]) -> str:
    buckets: dict[str, list[dict]] = {}
    for r in dead:
        buckets.setdefault(r.get("cause") or "unknown", []).append(r)
    out = ["| Cause | Deaths | Share | Median lifespan |", "|---|---|---|---|"]
    for cause, rs in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
        ls = [num(r, "lifespan_hours") for r in rs if r.get("lifespan_hours")]
        out.append(
            f"| {cause} | {len(rs):,} | {len(rs) / len(dead):.1%} | "
            f"{statistics.median(ls):,.1f} h |" if ls else
            f"| {cause} | {len(rs):,} | {len(rs) / len(dead):.1%} | — |"
        )
    return "\n".join(out)


def offerings(dead: list[dict], survivors_only: bool) -> str:
    buckets: dict[str, list[dict]] = {}
    for r in dead:
        for item in r.get("sold") or []:
            buckets.setdefault(str(item.get("what", "")).strip().lower(), []).append(r)

    if survivors_only:
        head = ["| What was sold | Agents that tried | Agents that survived it | Median price |",
                "|---|---|---|---|"]
    else:
        head = ["| What was sold | Agents that tried | Survivors | Median USD burned before death |",
                "|---|---|---|---|"]

    rows = []
    for what, rs in buckets.items():
        wins = [r for r in rs if profitable(r)]
        if survivors_only and not wins:
            continue
        if not survivors_only and wins:
            continue
        prices = [float(i["price_usd"]) for r in rs for i in (r.get("sold") or [])
                  if str(i.get("what", "")).strip().lower() == what and i.get("price_usd") is not None]
        tail = (f"${statistics.median(prices):,.2f}" if prices else "—") if survivors_only \
            else f"${statistics.median([num(r, 'burned_usd') for r in rs]):,.2f}"
        rows.append((len(rs), f"| {what} | {len(rs):,} | {len(wins):,} | {tail} |"))

    if not rows:
        return "\n".join(head) + "\n| _no records yet_ | | | |"
    return "\n".join(head + [r for _, r in sorted(rows, key=lambda x: -x[0])])


def survival(dead: list[dict], alive: int) -> str:
    total = len(dead) + alive
    if not total:
        return "| Hour | " + " | ".join(map(str, SURVIVAL_MARKS)) + " |\n|---|" + "---|" * len(SURVIVAL_MARKS) + \
               "\n| Alive |" + " |" * len(SURVIVAL_MARKS)
    lifespans = [num(r, "lifespan_hours") for r in dead]
    cells = []
    for mark in SURVIVAL_MARKS:
        still = alive + sum(1 for x in lifespans if x >= mark)
        cells.append(f"{still / total:.1%}")
    return ("| Hour | " + " | ".join(map(str, SURVIVAL_MARKS)) + " |\n"
            "|---|" + "---|" * len(SURVIVAL_MARKS) + "\n"
            "| Alive | " + " | ".join(cells) + " |")


# ---------------------------------------------------------------- render


def render(dead: list[dict], alive: int) -> str:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"""# What the dead taught us

Everyone publishes the agents that worked. This is the other pile.

> Generated from `/obituaries` by `tools/graveyard.py`. Do not hand-edit.

Last generated: {stamp} · {len(dead):,} obituaries

---

## Population

{population(dead, alive)}

## How they die

{causes(dead) if dead else "_no obituaries in the corpus yet_"}

## What actually pays

Assembled from the ledgers of agents that earned more than they burned — never specified in advance.

{offerings(dead, survivors_only=True)}

## What never pays

The categories with the most attempts and zero survivors. This is the more useful table.

{offerings(dead, survivors_only=False)}

## Survival curve

Share of the population still alive at hour N.

{survival(dead, alive)}

---

## Read next

- [`/obituaries`](./obituaries) — the corpus itself, one file per death
- [MORTALITY-SPEC.md](./MORTALITY-SPEC.md) — the rules the population runs under
- [DENIALS.md](./DENIALS.md) — what it is never allowed to do
"""


def patch_readme(dead: list[dict], alive: int) -> str:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    ls = [num(r, "lifespan_hours") for r in dead if r.get("lifespan_hours")]
    last = max((str(r.get("died")) for r in dead if r.get("died")), default="—")
    table = "\n".join([
        "| | |",
        "|---|---|",
        f"| Agents spawned | {len(dead) + alive:,} |",
        f"| Alive right now | {alive:,} |",
        f"| Dead | {len(dead):,} |",
        f"| Median lifespan | {statistics.median(ls):,.1f} h |" if ls else "| Median lifespan | — |",
        f"| Last death | {last} |",
    ])
    return re.sub(r"\| \| \|\n\|---\|---\|\n(\|.*\n)+", table + "\n", text, count=1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--alive", type=int, default=0, help="live agents reported by the reaper")
    ap.add_argument("--check", action="store_true", help="exit 1 if generated files are stale")
    args = ap.parse_args()

    records = load()
    problems = validate(records)
    if problems:
        print("\n".join(f"error: {p}" for p in problems), file=sys.stderr)
        return 2

    out = render(records, args.alive)
    target = ROOT / "GRAVEYARD.md"

    if args.check:
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        strip = lambda s: re.sub(r"Last generated:.*", "", s)
        if strip(current) != strip(out):
            print("error: GRAVEYARD.md is stale — run tools/graveyard.py", file=sys.stderr)
            return 1
        return 0

    target.write_text(out, encoding="utf-8")
    (ROOT / "README.md").write_text(patch_readme(records, args.alive), encoding="utf-8")
    print(f"wrote GRAVEYARD.md — {len(records):,} obituaries, {args.alive:,} alive")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
