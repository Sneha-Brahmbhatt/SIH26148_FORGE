# FORGE DSL Language Reference Manual

**FORGE — Forensic Object Runtime & Governed Execution**  
*Problem Statement SIH26148 | National Technical Research Organisation (NTRO)*

---

## 1. Safety Boundary Directive

> **MANDATORY STATEMENT:**  
> FORGE is intended only for authorized digital-forensic investigations and controlled security environments. It does not bypass, disable, evade, or interfere with endpoint security controls.

---

## 2. Core Concepts & Syntax Grammar

FORGE DSL is a forensic-native Domain Specific Language designed for capability-governed, policy-checked digital evidence extraction and analysis.

### Required Header Structure

Every valid FORGE script must start with a `CASE` declaration and explicit capability requirements:

```forge
CASE "CASE-001"

REQUIRE ANALYST "investigator@org.example"
REQUIRE POLICY "standard-read-only-v1"
REQUIRE CAPABILITIES [
    HOST_READ,
    PROCESS_READ,
    SERVICE_READ,
    FILE_READ,
    FILE_HASH,
    EVENT_READ,
    NETWORK_READ,
    PCAP_READ,
    TIMELINE_BUILD,
    FINDING_GENERATE,
    EXPORT_DATA,
    REPORT_GENERATE
]
```

---

## 3. Allowed Forensic Commands Registry

| Command | Required Capability | Parameter Description | Return Type | Usage Example |
|---|---|---|---|---|
| `CASE "ID"` | `CASE_MANAGE` | Case identifier string | `Statement` | `CASE "CASE-001"` |
| `REQUIRE ANALYST "email"` | `IDENTITY_ASSERT` | Analyst identifier string | `Statement` | `REQUIRE ANALYST "analyst@org.in"` |
| `REQUIRE POLICY "name"` | `POLICY_ASSERT` | Execution policy name | `Statement` | `REQUIRE POLICY "standard-read-only-v1"` |
| `REQUIRE CAPABILITIES [...]` | `CAPABILITY_ASSERT` | Array of capability identifiers | `Statement` | `REQUIRE CAPABILITIES [HOST_READ, FILE_READ]` |
| `HOST_INFO()` | `HOST_READ` | None | `HostInfoDict` | `host = HOST_INFO()` |
| `PROCESS_LIST()` | `PROCESS_READ` | None | `ProcessList` | `processes = PROCESS_LIST()` |
| `SERVICE_LIST()` | `SERVICE_READ` | None | `ServiceList` | `services = SERVICE_LIST()` |
| `SYSTEM_CONFIG()` | `SYSTEM_READ` | None | `SystemConfigDict` | `sys = SYSTEM_CONFIG()` |
| `USER_SESSIONS()` | `USER_READ` | None | `UserSessionsList` | `users = USER_SESSIONS()` |
| `FILE_LIST(path)` | `FILE_READ` | Dataset path string | `FilePathList` | `files = FILE_LIST("./datasets/computer/files")` |
| `FILE_METADATA(files)` | `FILE_READ` | File path array or string | `FileMetadataList` | `meta = FILE_METADATA(files)` |
| `HASH_FILES(files, algo)` | `FILE_HASH` | File list, hash algorithm string | `FileHashList` | `hashes = HASH_FILES(files, "SHA256")` |
| `EVENT_LOGS(source)` | `EVENT_READ` | Source channel ("System", "Security") | `EventLogsList` | `events = EVENT_LOGS("Security")` |
| `BROWSER_HISTORY()` | `ARTIFACT_READ` | None | `BrowserHistoryList` | `history = BROWSER_HISTORY()` |
| `REGISTRY_METADATA(keys)` | `REGISTRY_READ` | Registry key paths array | `RegistryList` | `reg = REGISTRY_METADATA()` |
| `PCAP_LOAD(path)` | `PCAP_READ` | PCAP / network capture dataset path | `PcapHandle` | `pcap = PCAP_LOAD("./datasets/network/sample.pcap")` |
| `NETWORK_CONNECTIONS(pcap)` | `NETWORK_READ` | PCAP handle | `ConnectionFlowList` | `conns = NETWORK_CONNECTIONS(pcap)` |
| `DNS_ACTIVITY(pcap)` | `NETWORK_READ` | PCAP handle | `DnsActivityList` | `dns = DNS_ACTIVITY(pcap)` |
| `PROTOCOL_STATS(pcap)` | `NETWORK_READ` | PCAP handle | `ProtocolStatsList` | `stats = PROTOCOL_STATS(pcap)` |
| `FLOW_SUMMARY(pcap)` | `NETWORK_READ` | PCAP handle | `FlowSummaryList` | `flows = FLOW_SUMMARY(pcap)` |
| `BUILD_TIMELINE(sources)` | `TIMELINE_BUILD` | Array of collected evidence objects | `TimelineList` | `timeline = BUILD_TIMELINE([processes, events, dns])` |
| `ANALYZE_FINDINGS(...)` | `FINDING_GENERATE` | Timeline, file hashes, dns activity | `FindingsList` | `findings = ANALYZE_FINDINGS(timeline, hashes, dns)` |
| `EXPORT_EVIDENCE(obj, path)` | `EXPORT_DATA` | Evidence object, export path | `ExportResult` | `EXPORT_EVIDENCE(hashes, "./exports/hashes.json")` |
| `EXPORT_REPORT(obj, path, fmt)`| `REPORT_GENERATE` | Findings, report path, format | `ReportResult` | `EXPORT_REPORT(findings, "./reports/CASE-001", "html")` |

---

## 4. Prohibited Capabilities (Always Blocked)

Execution Policy `standard-read-only-v1` permanently denies the following capabilities:

- `WRITE_EVIDENCE`
- `EXECUTE_PROCESS`
- `LOAD_DRIVER`
- `INJECT_CODE`
- `RAW_DEVICE_WRITE`
- `NETWORK_EGRESS`
- `DISABLE_SECURITY_CONTROL`
- `BYPASS_SECURITY_CONTROL`
