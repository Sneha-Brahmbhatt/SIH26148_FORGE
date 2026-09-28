"""
FORGE Computer Forensics - Browser History Artifact Collector
"""

import json
import os
from typing import List, Dict, Any

def collect_browser_history(dataset_path: str = "./datasets/computer/browser_history.json") -> List[Dict[str, Any]]:
    if os.path.exists(dataset_path):
        with open(dataset_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("history", [])

    return [
        {
            "id": 1,
            "url": "https://internal.corp.local/login",
            "title": "Corporate Single Sign-On",
            "visit_time_utc": "2026-09-25T14:05:10Z",
            "visit_count": 12,
            "browser": "Chrome"
        },
        {
            "id": 2,
            "url": "https://pastebin.org/raw/temp89342",
            "title": "Pastebin Raw Content",
            "visit_time_utc": "2026-09-25T14:14:02Z",
            "visit_count": 1,
            "browser": "Chrome"
        },
        {
            "id": 3,
            "url": "https://docs.python.org/3/library/ast.html",
            "title": "ast — Abstract Syntax Trees — Python documentation",
            "visit_time_utc": "2026-09-25T14:20:00Z",
            "visit_count": 5,
            "browser": "Chrome"
        }
    ]
