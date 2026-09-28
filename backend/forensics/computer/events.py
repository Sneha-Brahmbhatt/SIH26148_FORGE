"""
FORGE Computer Forensics - Windows Event Logs Collector
"""

import json
import os
from typing import List, Dict, Any

def collect_event_logs(source: str = "System", dataset_dir: str = "./datasets/computer") -> List[Dict[str, Any]]:
    file_map = {
        "System": "events_system.json",
        "Security": "events_security.json",
        "Application": "events_application.json"
    }

    target_file = os.path.join(dataset_dir, file_map.get(source, "events_system.json"))
    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("events", [])

    # Synthetic default events if dataset file not found
    if source == "Security":
        return [
            {
                "event_id": 4624,
                "provider": "Microsoft-Windows-Security-Auditing",
                "channel": "Security",
                "timestamp_utc": "2026-09-25T14:10:00Z",
                "task": "Logon",
                "level": "Information",
                "computer": "FORENSIC-TARGET-01",
                "message": "An account was successfully logged on. User: CORP\\john.doe (Logon Type: 2)",
                "data": {"TargetUserName": "john.doe", "LogonType": 2, "IpAddress": "127.0.0.1"}
            },
            {
                "event_id": 4688,
                "provider": "Microsoft-Windows-Security-Auditing",
                "channel": "Security",
                "timestamp_utc": "2026-09-25T14:15:22Z",
                "task": "Process Creation",
                "level": "Information",
                "computer": "FORENSIC-TARGET-01",
                "message": "A new process has been created: powershell.exe by svchost.exe",
                "data": {"NewProcessName": "powershell.exe", "CommandLine": "powershell.exe -ExecutionPolicy Bypass"}
            },
            {
                "event_id": 7045,
                "provider": "Service Control Manager",
                "channel": "System",
                "timestamp_utc": "2026-09-25T14:16:05Z",
                "task": "Service Installation",
                "level": "Warning",
                "computer": "FORENSIC-TARGET-01",
                "message": "A service was installed in the system: CustomUpdaterSvc",
                "data": {"ServiceName": "CustomUpdaterSvc", "ImagePath": "C:\\Users\\Public\\Downloads\\updater_svc.exe"}
            }
        ]

    return [
        {
            "event_id": 6005,
            "provider": "EventLog",
            "channel": "System",
            "timestamp_utc": "2026-09-25T08:00:00Z",
            "task": "System Startup",
            "level": "Information",
            "computer": "FORENSIC-TARGET-01",
            "message": "The Event log service was started.",
            "data": {}
        }
    ]
