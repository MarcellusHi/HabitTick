import datetime as dt
from src.habittick import calc_streak, Entry

def mk(ts):
    return Entry(ts=ts, habit="read")

def test_simple_streak():
    today=dt.date.today()
    entries=[
        mk((today).isoformat()+"T08:01:02"),
        mk((today-dt.timedelta(days=1)).isoformat()+"T22:12:44"),
        mk((today-dt.timedelta(days=2)).isoformat()+"T06:47:11"),
    ]
    assert calc_streak(entries, "read") >= 3
