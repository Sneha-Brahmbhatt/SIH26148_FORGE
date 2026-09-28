# FORGE 5-Minute SIH Demonstration Guide

**Problem Statement SIH26148 | National Technical Research Organisation (NTRO)**

---

## 1. Quick Demonstration Workflow (1-Click or Manual)

### Option A: One-Click SIH Demo Button
1. Open Dashboard at `http://localhost:5173`.
2. Click **"RUN 5-MINUTE SIH DEMO"**.
3. Observe live execution status, policy approval, evidence hashing, timeline correlation, findings, and audit log generation.

### Option B: Manual Step-by-Step Walkthrough
1. **Case Creation**: Navigate to **Case Management** and verify `CASE-001`.
2. **Script Editor**: Open **Script Editor**, select `demo_full_analysis.forge`.
3. **Validate Script**: Click **Validate Script** to view tokens, AST, semantic diagnostics, and capability policy approval (`APPROVED`).
4. **Test Policy Block**: Select `demo_policy_blocked.forge` and click **Validate Script**. Notice that the script requests `EXECUTE_PROCESS` & `WRITE_EVIDENCE` and is immediately marked `BLOCKED`.
5. **Execute Approved Script**: Switch back to `demo_full_analysis.forge` and click **Execute Analysis**.
6. **Inspect Evidence & Hashes**: Open **Evidence & Hashes** to view SHA-256 baseline records.
7. **Computer & Network Subsystems**: Explore **Computer Forensics** (host, processes, services, event logs) and **Network Forensics** (PCAP mode indicator, flow summaries, DNS telemetry).
8. **Unified Timeline & Findings**: Open **Unified Timeline** and **Findings** to view technical findings separating Observed Evidence vs Derived Analysis vs Investigator Review Required.
9. **Chain of Custody & Audit Trail**: Open **Chain of Custody** and **Audit Logs** to verify hash-chain integrity (`VERIFIED VALID`).
10. **Reports**: Open **Reports** to view or download generated JSON, CSV, and HTML reports.
