from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Candidate:
    match_id: str
    league: str
    home: str
    away: str
    market: str      # '1X2' / 'OU' 等
    selection: str   # 'H'/'D'/'A' 或 'Over2.5'
    odds: float
    prob: float      # 模型概率
    conf: float = 1.0  # 置信度（可选）

def kelly(p: float, odds: float, cap: float = 0.08) -> float:
    b = max(odds - 1.0, 1e-12)
    f = (b*p - (1-p)) / b
    return max(0.0, min(f, cap))

def filter_values(rows: List[Candidate],
                  ev_floor: float = 0.03,
                  kelly_cap: float = 0.08,
                  conf_min: float = 0.0) -> List[Dict]:
    picks = []
    for r in rows:
        ev = r.prob * r.odds - 1.0
        f  = kelly(r.prob, r.odds, kelly_cap)
        if ev >= ev_floor and r.conf >= conf_min and f > 0:
            picks.append({
                "match_id": r.match_id,
                "league": r.league,
                "home": r.home, "away": r.away,
                "market": r.market, "selection": r.selection,
                "odds": round(r.odds, 3),
                "prob": round(r.prob, 4),
                "ev": round(ev, 4),
                "kelly": round(f, 4)
            })
    picks.sort(key=lambda x: (x["ev"], x["prob"], x["league"]), reverse=True)
    return picks
