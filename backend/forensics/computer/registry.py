"""
FORGE Computer Forensics - Registry & Persistence Artifact Collector
"""

import json
import os
from typing import List, Dict, Any, Union

def collect_registry_metadata(keys_input: Union[List[str], str] = None, dataset_path: str = "./datasets/computer/registry_artifacts.json") -> List[Dict[str, Any]]:
    if os.path.exists(dataset_path):
        with open(dataset_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("registry_keys", [])

    return [
        {
            "hive": "HKCU",
            "key_path": "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            "value_name": "OneDrive",
            "value_type": "REG_SZ",
            "value_data": "C:\\Users\\john.doe\\AppData\\Local\\Microsoft\\OneDrive\\OneDrive.exe /background",
            "modified_time_utc": "2026-09-20T10:00:00Z"
        },
        {
            "hive": "HKLM",
            "key_path": "Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce",
            "value_name": "UpdateFix",
            "value_type": "REG_SZ",
            "value_data": "C:\\Users\\Public\\Downloads\\updater_svc.exe",
            "modified_time_utc": "2026-09-25T14:16:10Z"
        }
    ]
