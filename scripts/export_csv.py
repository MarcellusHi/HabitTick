#!/usr/bin/env python3
import csv,json,sys,os
from pathlib import Path
LOG=Path(os.path.expanduser('~/.habittick/log.jsonl'))
rows=[]
if LOG.exists():
    for line in LOG.read_text().splitlines():
        if not line.strip():
            continue
        try:
            d=json.loads(line)
        except Exception:
            continue
        rows.append([d.get('ts',''), d.get('habit',''), d.get('note','')])
writer=csv.writer(sys.stdout)
writer.writerow(["ts","habit","note"])
writer.writerows(rows)
