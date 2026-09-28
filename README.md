# FORGE — Forensic Object Runtime & Governed Execution

**Smart India Hackathon (SIH) 2026 Prototype**  
**Problem Statement SIH26148:** *"Creation of scripts/functions with new programming language to commence Computer & Network forensic analysis without triggering security solutions."*  
**Organization:** National Technical Research Organisation (NTRO)

---

> ### MANDATORY SAFETY BOUNDARY STATEMENT
> **FORGE is intended only for authorized digital-forensic investigations and controlled security environments. It does not bypass, disable, evade, or interfere with endpoint security controls.**

---

## 1. Problem Interpretation & Innovation Statement

### Problem Interpretation
"Without triggering security solutions" is interpreted strictly as:
> **Authorized digital forensic analysis that is verifiable, allow-listed, capability-limited, sandboxed, read-only, fully auditable, reproducible, and transparent to security teams.**

Endpoint and security controls remain active while authorized forensic workloads are explicitly trusted, constrained, and auditable.

### Unique Selling Proposition (USP)
> **"FORGE makes forensic safety structural: evidence is read-only by default, every script declares capabilities, every operation is policy-checked, every result is cryptographically provenance-bound, every execution is auditable, and every report is reproducible."**

The innovation lies in combining a **forensic-native DSL**, a **lexer → parser → AST → semantic validator pipeline**, a **capability-based permission model**, a **policy engine**, a **sandboxed runtime**, **read-only dataset access**, **SHA-256 evidence hashing**, **unified computer and network analysis**, and an **immutable hash-chained audit log**.

---

## 2. End-to-End Pipeline Architecture

```
Forensic Script (.forge)
       ↓
  [ Lexer ] ── Tokenizes source code (line & column tracking)
       ↓
  [ Parser ] ── Builds Abstract Syntax Tree (AST)
       ↓
  [ Semantic Validator ] ── Symbol table, arity, & argument type checks
       ↓
  [ Capability / Policy Engine ] ── Validates path boundaries & declared capabilities
       ↓
  [ Controlled Forensic Runtime ] ── Sandboxed execution against read-only datasets
       ↓
  [ Evidence & Provenance ] ── SHA-256 hashing & provenance record creation
       ↓
  [ Computer & Network Analysis ] ── Host, process, service, PCAP & DNS extraction
       ↓
  [ Timeline & Findings ] ── Chronological correlation & 3-part evidence breakdown
       ↓
  [ Hash-Chained Audit Trail ] ── Immutable record linking prev_audit_hash
       ↓
  [ Report Generation ] ── Reproducible JSON / CSV / HTML report generation
```

---

## 3. Technology Stack

- **Backend:** Python 3.11+, FastAPI, Uvicorn, SQLAlchemy 2.0, SQLite, Pydantic v2, Pytest, dpkt, Jinja2.
- **DSL Interpreter:** Custom-built Python Lexer, Recursive-Descent Parser, AST Builder, Semantic Validator, Policy Engine, and Controlled Runtime Sandbox. *(No eval, exec, subprocess, dynamic imports, or shell execution).*
- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons, Recharts, Dark SOC/DFIR Theme.
- **Deployment:** Docker, Docker Compose.

---

## 4. FORGE DSL Command Reference Table

| Command | Capability Required | Description | Example Syntax |
|---|---|---|---|
| `CASE "ID"` | `CASE_MANAGE` | Binds execution to a case ID | `CASE "CASE-001"` |
| `REQUIRE ANALYST "email"` | `IDENTITY_ASSERT` | Asserts analyst identity | `REQUIRE ANALYST "investigator@org.example"` |
| `REQUIRE POLICY "name"` | `POLICY_ASSERT` | Asserts policy version | `REQUIRE POLICY "standard-read-only-v1"` |
| `REQUIRE CAPABILITIES [...]` | `CAPABILITY_ASSERT` | Declares required capabilities | `REQUIRE CAPABILITIES [HOST_READ, FILE_READ]` |
| `HOST_INFO()` | `HOST_READ` | Host and OS metadata | `host_info = HOST_INFO()` |
| `PROCESS_LIST()` | `PROCESS_READ` | Process inventory | `processes = PROCESS_LIST()` |
| `SERVICE_LIST()` | `SERVICE_READ` | Service inventory | `services = SERVICE_LIST()` |
| `SYSTEM_CONFIG()` | `SYSTEM_READ` | System configuration | `system = SYSTEM_CONFIG()` |
| `USER_SESSIONS()` | `USER_READ` | User session metadata | `users = USER_SESSIONS()` |
| `FILE_LIST(path)` | `FILE_READ` | Lists controlled files | `files = FILE_LIST("./datasets/computer/files")` |
| `FILE_METADATA(files)` | `FILE_READ` | File metadata & timestamps | `file_metadata = FILE_METADATA(files)` |
| `HASH_FILES(files, algo)` | `FILE_HASH` | SHA-256 cryptographic baseline | `file_hashes = HASH_FILES(files, "SHA256")` |
| `EVENT_LOGS(source)` | `EVENT_READ` | Windows Event log parser | `events = EVENT_LOGS("System")` |
| `BROWSER_HISTORY()` | `ARTIFACT_READ` | Browser history artifacts | `history = BROWSER_HISTORY()` |
| `REGISTRY_METADATA(keys)` | `REGISTRY_READ` | Registry persistence artifacts | `registry = REGISTRY_METADATA()` |
| `PCAP_LOAD(path)` | `PCAP_READ` | PCAP / network capture dataset | `pcap = PCAP_LOAD("./datasets/network/sample.pcap")` |
| `NETWORK_CONNECTIONS(pcap)` | `NETWORK_READ` | Flow connection summaries | `connections = NETWORK_CONNECTIONS(pcap)` |
| `DNS_ACTIVITY(pcap)` | `NETWORK_READ` | DNS queries & NXDOMAIN ratios | `dns = DNS_ACTIVITY(pcap)` |
| `PROTOCOL_STATS(pcap)` | `NETWORK_READ` | Protocol distribution stats | `protocol_stats = PROTOCOL_STATS(pcap)` |
| `FLOW_SUMMARY(pcap)` | `NETWORK_READ` | Flow summary by IP/port | `flow_summary = FLOW_SUMMARY(pcap)` |
| `BUILD_TIMELINE(sources)` | `TIMELINE_BUILD` | Unified chronological timeline | `timeline = BUILD_TIMELINE([processes, dns])` |
| `ANALYZE_FINDINGS(...)` | `FINDING_GENERATE` | Evidence-backed findings | `findings = ANALYZE_FINDINGS(timeline, hashes, dns)` |
| `EXPORT_EVIDENCE(obj, path)` | `EXPORT_DATA` | Export evidence to JSON/CSV | `EXPORT_EVIDENCE(file_hashes, "./exports/hashes.json")` |
| `EXPORT_REPORT(obj, path, fmt)`| `REPORT_GENERATE` | Generate JSON/CSV/HTML report | `EXPORT_REPORT(findings, "./reports/CASE-001", "html")` |

### Always-Denied Prohibited Capabilities
`WRITE_EVIDENCE`, `EXECUTE_PROCESS`, `LOAD_DRIVER`, `INJECT_CODE`, `RAW_DEVICE_WRITE`, `NETWORK_EGRESS`, `DISABLE_SECURITY_CONTROL`, `BYPASS_SECURITY_CONTROL`.

---

## 5. Sample Safe Script vs Prohibited Script

### Approved Safe Script (`demo_full_analysis.forge`)
```forge
CASE "CASE-001"

REQUIRE ANALYST "investigator@org.example"
REQUIRE POLICY "standard-read-only-v1"
REQUIRE CAPABILITIES [
    HOST_READ,
    PROCESS_READ,
    SERVICE_READ,
    SYSTEM_READ,
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

host_info = HOST_INFO()
processes = PROCESS_LIST()
services = SERVICE_LIST()

files = FILE_LIST("./datasets/computer/files")
file_metadata = FILE_METADATA(files)
file_hashes = HASH_FILES(files, "SHA256")

events_system = EVENT_LOGS("System")
events_security = EVENT_LOGS("Security")

pcap = PCAP_LOAD("./datasets/network/sample.pcap")
connections = NETWORK_CONNECTIONS(pcap)
dns = DNS_ACTIVITY(pcap)

timeline = BUILD_TIMELINE([host_info, processes, services, file_metadata, events_system, events_security, connections, dns])
findings = ANALYZE_FINDINGS(timeline, file_hashes, dns)

EXPORT_EVIDENCE(file_hashes, "./exports/file_hashes.json")
EXPORT_REPORT(findings, "./reports/CASE-001-report", "html")
```

### Prohibited Script (`demo_policy_blocked.forge`)
```forge
CASE "CASE-BAD"

REQUIRE CAPABILITIES [
    WRITE_EVIDENCE,
    EXECUTE_PROCESS,
    DISABLE_SECURITY_CONTROL
]

EXECUTE_PROCESS("cmd.exe")
WRITE_EVIDENCE("./evidence/disk.E01", "modified")
```
**Policy Decision:** `BLOCKED` before execution start. Audit event `POLICY_DENIED` recorded.

---

## 6. Installation & Quick Start

### Option A: Local Development Run

1. **Backend Setup:**
   ```bash
   cd backend
   python -m venv .venv
   # Windows: .venv\Scripts\activate | Linux/macOS: source .venv/bin/activate
   pip install -r requirements.txt
   python -m app.seed
   uvicorn app.main:app --reload --port 8000
   ```

2. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Open browser at `http://localhost:5173`.

### Option B: Docker Compose

```bash
docker-compose up --build
```
- Backend runs on `http://localhost:8000`
- Frontend runs on `http://localhost:5173`

---

## 7. Running Tests

Run the complete Python backend test suite including the mandatory E2E test `test_full_sih_demo_workflow`:

```bash
cd backend
python -m pytest tests/
```

Output:
```
================ flex test session starts ================
collected 6 items

tests/test_full_sih_demo_workflow.py ..                                  [ 33%]
tests/test_lexer.py .                                                    [ 50%]
tests/test_parser.py .                                                   [ 66%]
tests/test_policy.py ..                                                  [100%]

================ 6 passed in 1.66s ================
```

---

## 8. Five-Minute SIH Demonstration Guide

1. Open Dashboard at `http://localhost:5173`.
2. Click **"RUN 5-MINUTE SIH DEMO"**.
3. View automatic execution progress across lexer, parser, AST, capability check, policy engine, sandboxed runtime, evidence collection, SHA-256 hashing, timeline correlation, findings, chain of custody, and HTML report generation.
4. Navigate to **Script Editor**, select `demo_policy_blocked.forge`, and click **Validate Script** to demonstrate policy blocking of prohibited capabilities.

---

## 9. Disclaimer & Synthetic Datasets

> **SYNTHETIC DATASET DISCLAIMER:**  
> All computer and network forensic datasets included in `datasets/` are synthetically generated for demonstration and testing of the SIH26148 FORGE prototype. No real host evidence, malware, or proprietary threat telemetry is included.
