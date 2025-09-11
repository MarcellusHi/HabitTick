#!/usr/bin/env python3
"""
HabitTick: Log habit ticks and inspect streaks.
Stores data as JSONL under ~/.habittick/log.jsonl
"""
from __future__ import annotations
import argparse, json, os, sys, datetime as dt
from dataclasses import dataclass, asdict
from pathlib import Path

LOG_DIR = Path(os.path.expanduser("~/.habittick"))
LOG_FILE = LOG_DIR / "log.jsonl"

@dataclass
class Entry:
    ts: str
    habit: str
    note: str | None = None

    @staticmethod
    def now(habit: str, note: str | None = None) -> "Entry":
        return Entry(ts=dt.datetime.now().isoformat(timespec='seconds'), habit=habit, note=note)

def ensure_paths() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        LOG_FILE.touch()

def append_entry(e: Entry) -> None:
    ensure_paths()
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(e), ensure_ascii=False) + "\n")

def read_entries() -> list[Entry]:
    if not LOG_FILE.exists():
        return []
    items: list[Entry] = []
    with LOG_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            try:
                d=json.loads(line)
                items.append(Entry(**d))
            except Exception:
                # ignore malformed lines
                continue
    return items

def calc_streak(entries: list[Entry], habit: str) -> int:
    days=set()
    for e in entries:
        if e.habit!=habit:
            continue
        try:
            d=e.ts[:10]
            days.add(d)
        except Exception:
            continue
    if not days:
        return 0
    today=dt.date.today()
    streak=0
    cur=today
    while cur.isoformat() in days:
        streak+=1
        cur = cur - dt.timedelta(days=1)
    return streak

def weekly_summary(entries: list[Entry], habit: str) -> dict:
    today=dt.date.today()
    start = today - dt.timedelta(days=6)
    counts={ (start+dt.timedelta(days=i)).isoformat():0 for i in range(7)}
    for e in entries:
        if e.habit!=habit:
            continue
        d=e.ts[:10]
        if d in counts:
            counts[d]+=1
    return counts

def cmd_log(args):
    append_entry(Entry.now(args.habit, args.note))
    print(f"Logged: {args.habit}" + (f" — {args.note}" if args.note else ""))

def cmd_streak(args):
    entries=read_entries()
    s=calc_streak(entries, args.habit)
    print(f"Streak for {args.habit}: {s}")

def cmd_week(args):
    entries=read_entries()
    counts=weekly_summary(entries, args.habit)
    for d,c in sorted(counts.items()):
        print(f"{d} {c}")

def build_parser():
    p=argparse.ArgumentParser(prog="habittick")
    sub=p.add_subparsers(dest="cmd", required=True)

    p_log=sub.add_parser("log")
    p_log.add_argument("habit")
    p_log.add_argument("--note")
    p_log.set_defaults(func=cmd_log)

    p_streak=sub.add_parser("streak")
    p_streak.add_argument("habit")
    p_streak.set_defaults(func=cmd_streak)

    p_week=sub.add_parser("week")
    p_week.add_argument("habit")
    p_week.set_defaults(func=cmd_week)
    return p

def main(argv=None):
    args=build_parser().parse_args(argv)
    args.func(args)

if __name__ == "__main__":
    main()
