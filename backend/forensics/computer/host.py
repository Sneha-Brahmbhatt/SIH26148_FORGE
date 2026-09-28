"""
FORGE Computer Forensics - Host Collector
"""

import json
import os

def collect_host_info(dataset_path: str = "./datasets/computer/host.json") -> dict:
    if os.path.exists(dataset_path):
        with open(dataset_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    # Fallback default synthetic host info
    return {
        "hostname": "FORENSIC-TARGET-01",
        "os": "Windows 11 Enterprise",
        "architecture": "x86_64",
        "timezone": "UTC+05:30",
        "boot_time_utc": "2026-09-25T08:00:00Z",
        "domain": "CORP.LOCAL",
        "ip_address": "192.168.1.105",
        "mac_address": "00:15:5D:01:A4:12",
        "dataset_version": "demo-dataset-v1",
        "synthetic": True
    }
