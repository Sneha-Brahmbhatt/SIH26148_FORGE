"""
FORGE Timeline Engine
Builds a unified, chronologically sorted timeline from computer and network evidence sources.
"""

from typing import List, Dict, Any

class TimelineBuilder:
    def __init__(self, case_id: str = "CASE-001", execution_id: str = "EXE-000001"):
        self.case_id = case_id
        self.execution_id = execution_id
        self.events: List[Dict[str, Any]] = []
        self.counter = 1

    def build_timeline(self, sources: List[Any]) -> List[Dict[str, Any]]:
        self.events.clear()
        self.counter = 1

        for src in sources:
            if not src:
                continue
            if isinstance(src, dict):
                self._process_item(src)
            elif isinstance(src, list):
                for item in src:
                    self._process_item(item)

        # Sort chronologically by timestamp_utc
        self.events.sort(key=lambda x: x.get("timestamp_utc", ""))
        return self.events

    def _process_item(self, item: Dict[str, Any]):
        evt_id = f"TL-{self.counter:05d}"
        self.counter += 1

        # Host info
        if "hostname" in item:
            self.events.append({
                "timeline_event_id": evt_id,
                "case_id": self.case_id,
                "execution_id": self.execution_id,
                "timestamp_utc": item.get("boot_time_utc", "2026-09-25T08:00:00Z"),
                "event_type": "SYSTEM",
                "source": "HOST_INFO",
                "title": f"Host Identified: {item.get('hostname')}",
                "description": f"OS: {item.get('os')}, Domain: {item.get('domain')}, IP: {item.get('ip_address')}",
                "evidence_id": item.get("evidence_id", "EVD-HOST"),
                "related_object": item.get("hostname"),
                "severity": "INFO",
                "synthetic": item.get("synthetic", True)
            })

        # Process item
        elif "pid" in item and "name" in item:
            severity = "INFO"
            if "powershell" in item.get("name", "").lower() and "bypass" in item.get("cmdline", "").lower():
                severity = "HIGH"
            elif "cmd.exe" in item.get("name", "").lower():
                severity = "MEDIUM"

            self.events.append({
                "timeline_event_id": evt_id,
                "case_id": self.case_id,
                "execution_id": self.execution_id,
                "timestamp_utc": item.get("start_time_utc", "2026-09-25T12:00:00Z"),
                "event_type": "PROCESS",
                "source": "PROCESS_LIST",
                "title": f"Process Start: {item.get('name')} (PID {item.get('pid')})",
                "description": f"Cmdline: {item.get('cmdline')} | User: {item.get('user')}",
                "evidence_id": item.get("evidence_id", "EVD-PROC"),
                "related_object": f"PID {item.get('pid')}",
                "severity": severity,
                "synthetic": True
            })

        # Service item
        elif "display_name" in item and "binary_path" in item:
            severity = "INFO"
            if "Users\\Public" in item.get("binary_path", ""):
                severity = "HIGH"

            self.events.append({
                "timeline_event_id": evt_id,
                "case_id": self.case_id,
                "execution_id": self.execution_id,
                "timestamp_utc": item.get("start_time_utc", "2026-09-25T14:16:05Z"),
                "event_type": "SYSTEM",
                "source": "SERVICE_LIST",
                "title": f"Service Registered: {item.get('name')}",
                "description": f"Display: {item.get('display_name')} | Binary: {item.get('binary_path')}",
                "evidence_id": item.get("evidence_id", "EVD-SVC"),
                "related_object": item.get("name"),
                "severity": severity,
                "synthetic": True
            })

        # File item
        elif "size_bytes" in item and "path" in item:
            severity = "INFO"
            if "temp" in item.get("path", "").lower() or "public" in item.get("path", "").lower():
                severity = "MEDIUM"

            self.events.append({
                "timeline_event_id": evt_id,
                "case_id": self.case_id,
                "execution_id": self.execution_id,
                "timestamp_utc": item.get("modified_at_utc", item.get("created_at_utc", "2026-09-25T14:15:00Z")),
                "event_type": "FILE",
                "source": "FILE_METADATA",
                "title": f"File Artifact: {item.get('name')}",
                "description": f"Path: {item.get('path')} | Size: {item.get('size_bytes')} bytes",
                "evidence_id": item.get("evidence_id", "EVD-FILE"),
                "related_object": item.get("path"),
                "severity": severity,
                "synthetic": True
            })

        # Event Log item
        elif "event_id" in item:
            severity = "INFO"
            if item.get("event_id") in (7045, 4688):
                severity = "MEDIUM"

            self.events.append({
                "timeline_event_id": evt_id,
                "case_id": self.case_id,
                "execution_id": self.execution_id,
                "timestamp_utc": item.get("timestamp_utc", "2026-09-25T14:10:00Z"),
                "event_type": "EVENT_LOG",
                "source": f"EVENT_LOG_{item.get('channel', 'System')}",
                "title": f"Event ID {item.get('event_id')} - {item.get('task', 'Log Event')}",
                "description": item.get("message"),
                "evidence_id": item.get("evidence_id", "EVD-EVT"),
                "related_object": f"EventID {item.get('event_id')}",
                "severity": severity,
                "synthetic": True
            })

        # DNS item
        elif "query_domain" in item:
            severity = "INFO"
            if item.get("response_code") == "NXDOMAIN" or "beacon" in item.get("query_domain", ""):
                severity = "HIGH"

            self.events.append({
                "timeline_event_id": evt_id,
                "case_id": self.case_id,
                "execution_id": self.execution_id,
                "timestamp_utc": item.get("timestamp_utc", "2026-09-25T14:15:15Z"),
                "event_type": "DNS",
                "source": "DNS_ACTIVITY",
                "title": f"DNS Query: {item.get('query_domain')}",
                "description": f"Client: {item.get('client_ip')} | Response: {item.get('response_code')} | Resolved: {item.get('resolved_ip')}",
                "evidence_id": item.get("evidence_id", "EVD-DNS"),
                "related_object": item.get("query_domain"),
                "severity": severity,
                "synthetic": True
            })

        # Network flow connection item
        elif "src_ip" in item and "dst_ip" in item:
            severity = "INFO"
            if item.get("dst_port") in (8443, 4444, 1337):
                severity = "HIGH"

            self.events.append({
                "timeline_event_id": evt_id,
                "case_id": self.case_id,
                "execution_id": self.execution_id,
                "timestamp_utc": item.get("timestamp_utc", "2026-09-25T14:15:25Z"),
                "event_type": "NETWORK",
                "source": "NETWORK_CONNECTIONS",
                "title": f"Network Flow: {item.get('src_ip')}:{item.get('src_port')} -> {item.get('dst_ip')}:{item.get('dst_port')}",
                "description": f"Protocol: {item.get('protocol')} | Bytes: {item.get('bytes')} | Packets: {item.get('packets')}",
                "evidence_id": item.get("evidence_id", "EVD-NET"),
                "related_object": f"{item.get('dst_ip')}:{item.get('dst_port')}",
                "severity": severity,
                "synthetic": True
            })

        # Registry item
        elif "hive" in item and "key_path" in item:
            severity = "INFO"
            if "RunOnce" in item.get("key_path", "") or "Public" in item.get("value_data", ""):
                severity = "HIGH"

            self.events.append({
                "timeline_event_id": evt_id,
                "case_id": self.case_id,
                "execution_id": self.execution_id,
                "timestamp_utc": item.get("modified_time_utc", "2026-09-25T14:16:10Z"),
                "event_type": "REGISTRY",
                "source": "REGISTRY_METADATA",
                "title": f"Registry Persistence Key: {item.get('value_name')}",
                "description": f"{item.get('hive')}\\{item.get('key_path')} -> {item.get('value_data')}",
                "evidence_id": item.get("evidence_id", "EVD-REG"),
                "related_object": item.get("value_name"),
                "severity": severity,
                "synthetic": True
            })

        # Browser item
        elif "url" in item and "title" in item:
            self.events.append({
                "timeline_event_id": evt_id,
                "case_id": self.case_id,
                "execution_id": self.execution_id,
                "timestamp_utc": item.get("visit_time_utc", "2026-09-25T14:14:02Z"),
                "event_type": "BROWSER",
                "source": "BROWSER_HISTORY",
                "title": f"Browser Visit: {item.get('title')}",
                "description": f"URL: {item.get('url')} | Browser: {item.get('browser')}",
                "evidence_id": item.get("evidence_id", "EVD-BRW"),
                "related_object": item.get("url"),
                "severity": "INFO",
                "synthetic": True
            })
