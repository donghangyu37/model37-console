import os
import importlib
import sys

def test_save_and_load_report_handles_bom(tmp_path, monkeypatch):
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    monkeypatch.setenv("REPORT_DIR", str(tmp_path))
    store = importlib.reload(importlib.import_module("store"))
    rows = [{
        "match_id": "M001",
        "league": "EPL",
        "home": "A",
        "away": "B",
        "market": "1X2",
        "selection": "H",
        "odds": 1.8,
        "prob": 0.6,
        "ev": 0.08,
        "kelly": 0.04,
    }]
    store.save_report(rows)
    loaded = store.load_report("today")
    assert loaded == rows
    assert "match_id" in loaded[0]
