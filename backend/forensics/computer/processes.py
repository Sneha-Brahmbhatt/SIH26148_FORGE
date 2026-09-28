"""
FORGE Computer Forensics - Process Collector
"""

import json
import os
from typing import List, Dict, Any

def collect_processes(dataset_path: str = "./datasets/computer/processes.json") -> List[Dict[str, Any]]:
    if os.path.exists(dataset_path):
        with open(dataset_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("processes", [])
    
    # Default synthetic process list
    return [
        {
            "pid": 4,
            "ppid": 0,
            "name": "System",
            "exe_path": "C:\\Windows\\System32\\ntoskrnl.exe",
            "user": "NT AUTHORITY\\SYSTEM",
            "start_time_utc": "2026-09-25T08:00:00Z",
            "cmdline": "System"
        },
        {
            "pid": 644,
            "ppid": 4,
            "name": "smss.exe",
            "exe_path": "C:\\Windows\\System32\\smss.exe",
            "user": "NT AUTHORITY\\SYSTEM",
            "start_time_utc": "2026-09-25T08:00:01Z",
            "cmdline": "\\SystemRoot\\System32\\smss.exe"
        },
        {
            "pid": 1024,
            "ppid": 644,
            "name": "svchost.exe",
            "exe_path": "C:\\Windows\\System32\\svchost.exe",
            "user": "NT AUTHORITY\\SYSTEM",
            "start_time_utc": "2026-09-25T08:00:05Z",
            "cmdline": "C:\\Windows\\system32\\svchost.exe -k netsvcs -p"
        },
        {
            "pid": 2840,
            "ppid": 1024,
            "name": "powershell.exe",
            "exe_path": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "user": "CORP\\john.doe",
            "start_time_utc": "2026-09-25T14:15:22Z",
            "cmdline": "powershell.exe -ExecutionPolicy Bypass -File C:\\Users\\john.doe\\AppData\\Local\\Temp\\update_script.ps1"
        },
        {
            "pid": 3110,
            "ppid": 2840,
            "name": "cmd.exe",
            "exe_path": "C:\\Windows\\System32\\cmd.exe",
            "user": "CORP\\john.doe",
            "start_time_utc": "2026-09-25T14:15:30Z",
            "cmdline": "cmd.exe /c whoami /all"
        }
    ]
