# FORGE System Architecture & Pipeline Design

**FORGE — Forensic Object Runtime & Governed Execution**

---

## 1. End-to-End Compiler & Execution Pipeline

```
Forensic Script
       ↓
  [ Lexer ] ── Token Stream (Line & Column Tracking)
       ↓
  [ Parser ] ── Abstract Syntax Tree (AST) Construction
       ↓
  [ Semantic Validator ] ── Symbol Table, Arity & Type Checks
       ↓
  [ Policy Engine ] ── Capability Matching & Path Sandbox Boundary Verification
       ↓
  [ Controlled Runtime ] ── Policy-Checked Read-Only Sandbox Execution
       ↓
  [ Evidence & Provenance ] ── SHA-256 Hashing & Immutable Hash-Chained Audit Logging
       ↓
  [ Forensic Analysis ] ── Unified Computer & Network Correlation
       ↓
  [ Timeline & Findings ] ── Chronological Correlation & 3-Part Findings Engine
       ↓
  [ Report Generation ] ── Reproducible JSON / CSV / HTML Reports
```

---

## 2. Component Subsystems

### Backend Subsystems (`backend/`)
1. **Language Interpreter (`backend/language/`)**: Real Python-implemented Lexer, Recursive-Descent Parser, AST Builder, Semantic Validator, Capability Analyzer, Policy Engine, and Sandboxed Runtime.
2. **Computer Forensics (`backend/forensics/computer/`)**: Host info, process list, service list, file metadata & SHA-256 baseline, event log parser (System, Security, Application), registry persistence artifact extractor, and browser history parser.
3. **Network Forensics (`backend/forensics/network/`)**: PCAP packet analyzer (`dpkt`/`scapy`) with fallback synthetic network dataset analyzer mode (`PCAP Mode: REAL SAMPLE PCAP` / `PCAP Mode: SYNTHETIC NETWORK DATASET`).
4. **Timeline & Findings (`backend/forensics/timeline/`, `backend/forensics/findings/`)**: Normalizes timestamps into unified chronological timeline and correlates findings separating Observed Evidence vs Derived Analysis vs Investigator Review Required.
5. **Evidence, Provenance & Audit (`backend/forensics/evidence/`)**: Creates evidence records, provenance objects, and maintains an append-only hash-chained audit log (`prev_audit_hash`, `audit_hash`).
6. **Reporting Engine (`backend/forensics/reporting/`)**: Jinja2 & CSV report generator with mandatory safety boundary and dataset disclaimer statements.

### Frontend Subsystems (`frontend/`)
- React 18, TypeScript, Vite, Tailwind CSS dark SOC/DFIR theme.
- 14 dedicated views for complete operational visibility from script editing to validation, execution, evidence, computer/network sub-systems, timeline, findings, chain of custody, reports, audit logs, and language reference.
