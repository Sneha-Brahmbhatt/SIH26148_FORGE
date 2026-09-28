"""
FORGE Seed & Dataset Initializer
Creates controlled synthetic computer and network datasets and seeds initial DB cases/scripts.
"""

import os
import json

DATASET_META = {
    "dataset_version": "demo-dataset-v1",
    "synthetic": True,
    "label": "SYNTHETIC / DEMONSTRATION DATA",
    "generated_for": "SIH26148 FORGE prototype"
}

def seed_datasets():
    comp_dir = "./datasets/computer"
    net_dir = "./datasets/network"
    files_dir = "./datasets/computer/files"
    os.makedirs(comp_dir, exist_ok=True)
    os.makedirs(net_dir, exist_ok=True)
    os.makedirs(files_dir, exist_ok=True)
    os.makedirs("./exports", exist_ok=True)
    os.makedirs("./reports", exist_ok=True)

    # 1. Host dataset
    host_file = os.path.join(comp_dir, "host.json")
    if not os.path.exists(host_file):
        with open(host_file, "w", encoding="utf-8") as f:
            json.dump({
                **DATASET_META,
                "hostname": "FORENSIC-TARGET-01",
                "os": "Windows 11 Enterprise (Build 22631)",
                "architecture": "x86_64",
                "timezone": "UTC+05:30",
                "boot_time_utc": "2026-09-25T08:00:00Z",
                "domain": "CORP.LOCAL",
                "ip_address": "192.168.1.105",
                "mac_address": "00:15:5D:01:A4:12"
            }, f, indent=2)

    # 2. Processes dataset
    proc_file = os.path.join(comp_dir, "processes.json")
    if not os.path.exists(proc_file):
        with open(proc_file, "w", encoding="utf-8") as f:
            json.dump({
                **DATASET_META,
                "processes": [
                    {"pid": 4, "ppid": 0, "name": "System", "exe_path": "C:\\Windows\\System32\\ntoskrnl.exe", "user": "NT AUTHORITY\\SYSTEM", "start_time_utc": "2026-09-25T08:00:00Z", "cmdline": "System"},
                    {"pid": 644, "ppid": 4, "name": "smss.exe", "exe_path": "C:\\Windows\\System32\\smss.exe", "user": "NT AUTHORITY\\SYSTEM", "start_time_utc": "2026-09-25T08:00:01Z", "cmdline": "\\SystemRoot\\System32\\smss.exe"},
                    {"pid": 1024, "ppid": 644, "name": "svchost.exe", "exe_path": "C:\\Windows\\System32\\svchost.exe", "user": "NT AUTHORITY\\SYSTEM", "start_time_utc": "2026-09-25T08:00:05Z", "cmdline": "C:\\Windows\\system32\\svchost.exe -k netsvcs -p"},
                    {"pid": 2840, "ppid": 1024, "name": "powershell.exe", "exe_path": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", "user": "CORP\\john.doe", "start_time_utc": "2026-09-25T14:15:22Z", "cmdline": "powershell.exe -ExecutionPolicy Bypass -File C:\\Users\\john.doe\\AppData\\Local\\Temp\\update_script.ps1"},
                    {"pid": 3110, "ppid": 2840, "name": "cmd.exe", "exe_path": "C:\\Windows\\System32\\cmd.exe", "user": "CORP\\john.doe", "start_time_utc": "2026-09-25T14:15:30Z", "cmdline": "cmd.exe /c whoami /all"}
                ]
            }, f, indent=2)

    # 3. Services dataset
    svc_file = os.path.join(comp_dir, "services.json")
    if not os.path.exists(svc_file):
        with open(svc_file, "w", encoding="utf-8") as f:
            json.dump({
                **DATASET_META,
                "services": [
                    {"name": "wuauserv", "display_name": "Windows Update", "state": "RUNNING", "start_type": "AUTOMATIC", "binary_path": "C:\\Windows\\system32\\svchost.exe -k netsvcs -p", "account": "LocalSystem"},
                    {"name": "WinDefend", "display_name": "Microsoft Defender Antivirus Service", "state": "RUNNING", "start_type": "AUTOMATIC", "binary_path": "C:\\ProgramData\\Microsoft\\Windows Defender\\Platform\\4.18.23110.3-0\\MsMpEng.exe", "account": "NT AUTHORITY\\SYSTEM"},
                    {"name": "CustomUpdaterSvc", "display_name": "Background System Update Helper", "state": "RUNNING", "start_type": "AUTOMATIC", "binary_path": "C:\\Users\\Public\\Downloads\\updater_svc.exe", "account": "LocalSystem"}
                ]
            }, f, indent=2)

    # 4. Events System dataset
    sys_ev_file = os.path.join(comp_dir, "events_system.json")
    if not os.path.exists(sys_ev_file):
        with open(sys_ev_file, "w", encoding="utf-8") as f:
            json.dump({
                **DATASET_META,
                "events": [
                    {"event_id": 6005, "provider": "EventLog", "channel": "System", "timestamp_utc": "2026-09-25T08:00:00Z", "task": "System Startup", "level": "Information", "computer": "FORENSIC-TARGET-01", "message": "The Event log service was started.", "data": {}},
                    {"event_id": 7045, "provider": "Service Control Manager", "channel": "System", "timestamp_utc": "2026-09-25T14:16:05Z", "task": "Service Installation", "level": "Warning", "computer": "FORENSIC-TARGET-01", "message": "A service was installed in the system: CustomUpdaterSvc", "data": {"ServiceName": "CustomUpdaterSvc", "ImagePath": "C:\\Users\\Public\\Downloads\\updater_svc.exe"}}
                ]
            }, f, indent=2)

    # 5. Events Security dataset
    sec_ev_file = os.path.join(comp_dir, "events_security.json")
    if not os.path.exists(sec_ev_file):
        with open(sec_ev_file, "w", encoding="utf-8") as f:
            json.dump({
                **DATASET_META,
                "events": [
                    {"event_id": 4624, "provider": "Microsoft-Windows-Security-Auditing", "channel": "Security", "timestamp_utc": "2026-09-25T14:10:00Z", "task": "Logon", "level": "Information", "computer": "FORENSIC-TARGET-01", "message": "An account was successfully logged on. User: CORP\\john.doe (Logon Type: 2)", "data": {"TargetUserName": "john.doe", "LogonType": 2}},
                    {"event_id": 4688, "provider": "Microsoft-Windows-Security-Auditing", "channel": "Security", "timestamp_utc": "2026-09-25T14:15:22Z", "task": "Process Creation", "level": "Information", "computer": "FORENSIC-TARGET-01", "message": "A new process has been created: powershell.exe by svchost.exe", "data": {"NewProcessName": "powershell.exe", "CommandLine": "powershell.exe -ExecutionPolicy Bypass"}}
                ]
            }, f, indent=2)

    # 6. Browser History dataset
    brw_file = os.path.join(comp_dir, "browser_history.json")
    if not os.path.exists(brw_file):
        with open(brw_file, "w", encoding="utf-8") as f:
            json.dump({
                **DATASET_META,
                "history": [
                    {"id": 1, "url": "https://internal.corp.local/login", "title": "Corporate Single Sign-On", "visit_time_utc": "2026-09-25T14:05:10Z", "visit_count": 12, "browser": "Chrome"},
                    {"id": 2, "url": "https://pastebin.org/raw/temp89342", "title": "Pastebin Raw Content", "visit_time_utc": "2026-09-25T14:14:02Z", "visit_count": 1, "browser": "Chrome"},
                    {"id": 3, "url": "https://docs.python.org/3/library/ast.html", "title": "ast — Abstract Syntax Trees — Python documentation", "visit_time_utc": "2026-09-25T14:20:00Z", "visit_count": 5, "browser": "Chrome"}
                ]
            }, f, indent=2)

    # 7. Registry Artifacts dataset
    reg_file = os.path.join(comp_dir, "registry_artifacts.json")
    if not os.path.exists(reg_file):
        with open(reg_file, "w", encoding="utf-8") as f:
            json.dump({
                **DATASET_META,
                "registry_keys": [
                    {"hive": "HKCU", "key_path": "Software\\Microsoft\\Windows\\CurrentVersion\\Run", "value_name": "OneDrive", "value_type": "REG_SZ", "value_data": "C:\\Users\\john.doe\\AppData\\Local\\Microsoft\\OneDrive\\OneDrive.exe /background", "modified_time_utc": "2026-09-20T10:00:00Z"},
                    {"hive": "HKLM", "key_path": "Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce", "value_name": "UpdateFix", "value_type": "REG_SZ", "value_data": "C:\\Users\\Public\\Downloads\\updater_svc.exe", "modified_time_utc": "2026-09-25T14:16:10Z"}
                ]
            }, f, indent=2)

    # 8. Sample files in files_dir
    sample_files = {
        "system_info.txt": "FORGE FORENSIC TARGET BUILD 22631\nOS: Windows 11 Enterprise\n",
        "update_script.ps1": "# Synthetic harmless script\nGet-Process | Select-Object Name, Id\n",
        "updater_svc.exe.txt": "SYNTHETIC BINARY DEMO FILE FOR HASHING\n",
        "network_config.json": json.dumps({"dhcp": True, "ip": "192.168.1.105", "gateway": "192.168.1.1"}, indent=2)
    }

    for fname, content in sample_files.items():
        fpath = os.path.join(files_dir, fname)
        if not os.path.exists(fpath):
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)

    # 9. Network dataset
    net_file = os.path.join(net_dir, "network_records.json")
    if not os.path.exists(net_file):
        with open(net_file, "w", encoding="utf-8") as f:
            json.dump({
                **DATASET_META,
                "mode": "SYNTHETIC NETWORK DATASET",
                "packet_count": 1420,
                "connections": [
                    {"id": "FLOW-001", "timestamp_utc": "2026-09-25T14:02:10Z", "src_ip": "192.168.1.105", "src_port": 51234, "dst_ip": "10.0.0.5", "dst_port": 53, "protocol": "UDP", "bytes": 342, "packets": 4},
                    {"id": "FLOW-002", "timestamp_utc": "2026-09-25T14:15:25Z", "src_ip": "192.168.1.105", "src_port": 58921, "dst_ip": "198.51.100.44", "dst_port": 8443, "protocol": "TCP", "bytes": 45120, "packets": 86},
                    {"id": "FLOW-003", "timestamp_utc": "2026-09-25T14:15:30Z", "src_ip": "192.168.1.105", "src_port": 58922, "dst_ip": "203.0.113.88", "dst_port": 443, "protocol": "TCP", "bytes": 12840, "packets": 32},
                    {"id": "FLOW-004", "timestamp_utc": "2026-09-25T14:16:02Z", "src_ip": "192.168.1.105", "src_port": 58925, "dst_ip": "198.51.100.44", "dst_port": 8443, "protocol": "TCP", "bytes": 38400, "packets": 70}
                ],
                "dns_activity": [
                    {"timestamp_utc": "2026-09-25T14:02:10Z", "query_domain": "internal.corp.local", "query_type": "A", "response_code": "NOERROR", "resolved_ip": "10.0.0.5", "client_ip": "192.168.1.105"},
                    {"timestamp_utc": "2026-09-25T14:15:15Z", "query_domain": "update.beacon-srv-test.net", "query_type": "A", "response_code": "NOERROR", "resolved_ip": "198.51.100.44", "client_ip": "192.168.1.105"},
                    {"timestamp_utc": "2026-09-25T14:15:18Z", "query_domain": "sub12.beacon-srv-test.net", "query_type": "A", "response_code": "NXDOMAIN", "resolved_ip": None, "client_ip": "192.168.1.105"},
                    {"timestamp_utc": "2026-09-25T14:15:20Z", "query_domain": "sub14.beacon-srv-test.net", "query_type": "A", "response_code": "NXDOMAIN", "resolved_ip": None, "client_ip": "192.168.1.105"}
                ],
                "protocol_stats": [
                    {"protocol": "TCP", "count": 1050, "percentage": 73.9},
                    {"protocol": "UDP", "count": 280, "percentage": 19.7},
                    {"protocol": "DNS", "count": 60, "percentage": 4.2},
                    {"protocol": "HTTP/HTTPS", "count": 30, "percentage": 2.2}
                ]
            }, f, indent=2)

if __name__ == "__main__":
    seed_datasets()
    print("[+] Datasets initialized successfully.")
