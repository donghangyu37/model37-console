from typing import List, Dict
from value_filter import Candidate, filter_values
import random, time
from store import save_report

# === 你现有代码的对接点（按需替换以下三个函数） ===

def fetch_today_fixtures_and_odds() -> List[Candidate]:
    """返回 Candidate 列表：示例随机数据。"""
    demo = []
    leagues = ["EPL","LaLiga","SerieA","J-League"]
    teams = [("Chelsea","Brentford"), ("Liverpool","Newcastle"),
             ("Urawa","Tokyo Verdy"), ("Kawasaki","Kashima") ]
    markets = [("1X2","H"), ("1X2","A"), ("OU","Over2.5") ]
    for i in range(12):
        home, away = random.choice(teams)
        league = random.choice(leagues)
        market, sel = random.choice(markets)
        odds = round(random.uniform(1.6, 3.2), 2)
        prob = round(random.uniform(0.35, 0.7), 4)  # 假装来自你的模型
        demo.append(Candidate(
            match_id=f"M{i:03d}", league=league, home=home, away=away,
            market=market, selection=sel, odds=odds, prob=prob, conf=1.0
        ))
    return demo

def run_model_prediction(cands: List[Candidate]) -> List[Candidate]:
    """如果概率另算，这里可以覆盖 prob/conf。当前示例直接返回。"""
    time.sleep(0.2)
    return cands

def select_value_rows(cands: List[Candidate]) -> List[Dict]:
    """价值筛选与排序（阈值可先固定，之后接入配置/GUI）。返回一个由字典组成的列表。"""
    return filter_values(cands, ev_floor=0.03, kelly_cap=0.08, conf_min=0.0)

# === 一键跑今天的完整流程 ===

def run_today_all() -> dict:
    raw = fetch_today_fixtures_and_odds()
    pred = run_model_prediction(raw)
    picks = select_value_rows(pred)
    path = save_report(picks)
    return {"count": len(picks), "report": path, "picks": picks}
