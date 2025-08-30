import os, pandas as pd
from datetime import datetime

REPORT_DIR = os.getenv("REPORT_DIR", "./reports")
os.makedirs(REPORT_DIR, exist_ok=True)

def report_path(day: str = "today") -> str:
    if day == "today":
        fname = datetime.now().strftime("%Y-%m-%d") + ".csv"
    else:
        fname = f"{day}.csv"
    return os.path.join(REPORT_DIR, fname)

def save_report(rows):
    df = pd.DataFrame(rows)
    p = report_path("today")
    df.to_csv(p, index=False, encoding="utf-8-sig")
    return p

def load_report(day: str = "today"):
    p = report_path(day)
    if not os.path.exists(p):
        return []
    df = pd.read_csv(p, encoding="utf-8-sig")
    return df.to_dict(orient="records")
