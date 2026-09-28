"""
FORGE Computer Forensics - Service Collector
"""

import json
import os
from typing import List, Dict, Any

def collect_services(dataset_path: str = "./datasets/computer/services.json") -> List[Dict[str, Any]]:
    if os.path.exists(dataset_path):
        with open(dataset_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("services", [])
            
    return [
        {
            "name": "wuauserv",
            "display_name": "Windows Update",
            "state": "RUNNING",
            "start_type": "AUTOMATIC",
            "binary_path": "C:\\Windows\\system32\\svchost.exe -k netsvcs -p",
            "account": "LocalSystem"
        },
        {
            "name": "WinDefend",
            "display_name": "Microsoft Defender Antivirus Service",
            "state": "RUNNING",
            "start_type": "AUTOMATIC",
            "binary_path": "C:\\ProgramData\\Microsoft\\Windows Defender\\Platform\\4.18.23110.3-0\\MsMpEng.exe",
            "account": "NT AUTHORITY\\SYSTEM"
        },
        {
            "name": "CustomUpdaterSvc",
            "display_name": "Background System Update Helper",
            "state": "RUNNING",
            "start_type": "AUTOMATIC",
            "binary_path": "C:\\Users\\Public\\Downloads\\updater_svc.exe",
            "account": "LocalSystem"
        }
    ]
