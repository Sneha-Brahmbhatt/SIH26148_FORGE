"""
FORGE Network Forensics - PCAP & Network Dataset Analyzer
Supports dual-mode execution:
1. REAL SAMPLE PCAP (parsed via dpkt or scapy if valid .pcap file exists)
2. SYNTHETIC NETWORK DATASET (fallback structured dataset mode)
"""

import os
import json

class NetworkAnalyzer:
    def __init__(self, target_path: str = "./datasets/network/sample.pcap"):
        self.target_path = target_path
        self.mode = "SYNTHETIC NETWORK DATASET"
        self.raw_data = None
        self._load()

    def _load(self):
        # Check if real pcap exists
        if os.path.exists(self.target_path) and self.target_path.endswith(".pcap"):
            try:
                import dpkt
                with open(self.target_path, "rb") as f:
                    pcap = dpkt.pcap.Reader(f)
                    self.mode = "REAL SAMPLE PCAP"
                    self.raw_data = self._parse_dpkt(pcap)
                    return
            except Exception:
                pass

        # Fallback to structured synthetic network JSON dataset
        json_path = os.path.join(os.path.dirname(self.target_path), "network_records.json")
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                self.raw_data = json.load(f)
                self.mode = "SYNTHETIC NETWORK DATASET"
                return

        # Default inline synthetic dataset
        self.mode = "SYNTHETIC NETWORK DATASET"
        self.raw_data = self._get_default_synthetic_network_data()

    def _parse_dpkt(self, pcap) -> dict:
        import dpkt
        import socket

        connections = []
        dns_activity = []
        protocols = {"TCP": 0, "UDP": 0, "ICMP": 0, "DNS": 0, "HTTP": 0, "OTHER": 0}

        packet_count = 0
        for ts, buf in pcap:
            packet_count += 1
            try:
                eth = dpkt.ethernet.Ethernet(buf)
                if not isinstance(eth.data, dpkt.ip.IP):
                    continue
                ip = eth.data
                src_ip = socket.inet_ntoa(ip.src)
                dst_ip = socket.inet_ntoa(ip.dst)

                proto_name = "OTHER"
                src_port = 0
                dst_port = 0

                if isinstance(ip.data, dpkt.tcp.TCP):
                    tcp = ip.data
                    src_port, dst_port = tcp.sport, tcp.dport
                    proto_name = "TCP"
                    protocols["TCP"] += 1
                    if dst_port == 80 or src_port == 80:
                        protocols["HTTP"] += 1
                elif isinstance(ip.data, dpkt.udp.UDP):
                    udp = ip.data
                    src_port, dst_port = udp.sport, udp.dport
                    proto_name = "UDP"
                    protocols["UDP"] += 1
                    if dst_port == 53 or src_port == 53:
                        protocols["DNS"] += 1
                        try:
                            dns = dpkt.dns.DNS(udp.data)
                            for q in dns.qd:
                                dns_activity.append({
                                    "timestamp_utc": "2026-09-25T14:15:10Z",
                                    "query_domain": q.name,
                                    "query_type": "A",
                                    "response_code": "NXDOMAIN" if dns.rcode == dpkt.dns.DNS_RCODE_NXDOMAIN else "NOERROR",
                                    "client_ip": src_ip
                                })
                        except Exception:
                            pass

                connections.append({
                    "id": f"CONN-{packet_count:04d}",
                    "timestamp_utc": "2026-09-25T14:15:10Z",
                    "src_ip": src_ip,
                    "src_port": src_port,
                    "dst_ip": dst_ip,
                    "dst_port": dst_port,
                    "protocol": proto_name,
                    "bytes": len(buf),
                    "packets": 1
                })
            except Exception:
                continue

        return {
            "mode": "REAL SAMPLE PCAP",
            "pcap_file": self.target_path,
            "packet_count": packet_count,
            "connections": connections,
            "dns_activity": dns_activity,
            "protocol_stats": protocols
        }

    def _get_default_synthetic_network_data(self) -> dict:
        return {
            "mode": "SYNTHETIC NETWORK DATASET",
            "pcap_file": self.target_path,
            "packet_count": 1420,
            "dataset_version": "demo-dataset-v1",
            "synthetic": True,
            "connections": [
                {
                    "id": "FLOW-001",
                    "timestamp_utc": "2026-09-25T14:02:10Z",
                    "src_ip": "192.168.1.105",
                    "src_port": 51234,
                    "dst_ip": "10.0.0.5",
                    "dst_port": 53,
                    "protocol": "UDP",
                    "bytes": 342,
                    "packets": 4
                },
                {
                    "id": "FLOW-002",
                    "timestamp_utc": "2026-09-25T14:15:25Z",
                    "src_ip": "192.168.1.105",
                    "src_port": 58921,
                    "dst_ip": "198.51.100.44",
                    "dst_port": 8443,
                    "protocol": "TCP",
                    "bytes": 45120,
                    "packets": 86
                },
                {
                    "id": "FLOW-003",
                    "timestamp_utc": "2026-09-25T14:15:30Z",
                    "src_ip": "192.168.1.105",
                    "src_port": 58922,
                    "dst_ip": "203.0.113.88",
                    "dst_port": 443,
                    "protocol": "TCP",
                    "bytes": 12840,
                    "packets": 32
                },
                {
                    "id": "FLOW-004",
                    "timestamp_utc": "2026-09-25T14:16:02Z",
                    "src_ip": "192.168.1.105",
                    "src_port": 58925,
                    "dst_ip": "198.51.100.44",
                    "dst_port": 8443,
                    "protocol": "TCP",
                    "bytes": 38400,
                    "packets": 70
                }
            ],
            "dns_activity": [
                {
                    "timestamp_utc": "2026-09-25T14:02:10Z",
                    "query_domain": "internal.corp.local",
                    "query_type": "A",
                    "response_code": "NOERROR",
                    "resolved_ip": "10.0.0.5",
                    "client_ip": "192.168.1.105"
                },
                {
                    "timestamp_utc": "2026-09-25T14:15:15Z",
                    "query_domain": "update.beacon-srv-test.net",
                    "query_type": "A",
                    "response_code": "NOERROR",
                    "resolved_ip": "198.51.100.44",
                    "client_ip": "192.168.1.105"
                },
                {
                    "timestamp_utc": "2026-09-25T14:15:18Z",
                    "query_domain": "sub12.beacon-srv-test.net",
                    "query_type": "A",
                    "response_code": "NXDOMAIN",
                    "resolved_ip": None,
                    "client_ip": "192.168.1.105"
                },
                {
                    "timestamp_utc": "2026-09-25T14:15:20Z",
                    "query_domain": "sub14.beacon-srv-test.net",
                    "query_type": "A",
                    "response_code": "NXDOMAIN",
                    "resolved_ip": None,
                    "client_ip": "192.168.1.105"
                }
            ],
            "protocol_stats": [
                {"protocol": "TCP", "count": 1050, "percentage": 73.9},
                {"protocol": "UDP", "count": 280, "percentage": 19.7},
                {"protocol": "DNS", "count": 60, "percentage": 4.2},
                {"protocol": "HTTP/HTTPS", "count": 30, "percentage": 2.2}
            ]
        }

    def get_pcap_info(self) -> dict:
        return {
            "mode": f"PCAP Mode: {self.mode}",
            "target_path": self.target_path,
            "packet_count": self.raw_data.get("packet_count", 0),
            "synthetic": self.raw_data.get("synthetic", True)
        }

    def get_connections(self) -> list:
        return self.raw_data.get("connections", [])

    def get_dns_activity(self) -> list:
        return self.raw_data.get("dns_activity", [])

    def get_protocol_stats(self) -> list:
        stats = self.raw_data.get("protocol_stats", [])
        if isinstance(stats, dict):
            total = sum(stats.values()) or 1
            return [
                {"protocol": k, "count": v, "percentage": round((v / total) * 100, 1)}
                for k, v in stats.items()
            ]
        return stats

    def get_flow_summary(self) -> list:
        conns = self.get_connections()
        flows = {}
        for c in conns:
            key = f"{c['src_ip']} -> {c['dst_ip']}:{c['dst_port']} ({c['protocol']})"
            if key not in flows:
                flows[key] = {
                    "flow_key": key,
                    "src_ip": c["src_ip"],
                    "dst_ip": c["dst_ip"],
                    "dst_port": c["dst_port"],
                    "protocol": c["protocol"],
                    "total_bytes": 0,
                    "total_packets": 0,
                    "connection_count": 0
                }
            flows[key]["total_bytes"] += c.get("bytes", 0)
            flows[key]["total_packets"] += c.get("packets", 1)
            flows[key]["connection_count"] += 1
        return list(flows.values())
