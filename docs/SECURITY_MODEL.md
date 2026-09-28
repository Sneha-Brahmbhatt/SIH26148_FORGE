# FORGE Security Model & Governed Execution Policy

**FORGE — Forensic Object Runtime & Governed Execution**

---

## 1. Safety Boundary & Non-Evasion Guarantee

> **MANDATORY SECURITY STATEMENT:**  
> FORGE is intended only for authorized digital-forensic investigations and controlled security environments. It does not bypass, disable, evade, or interfere with endpoint security controls.

---

## 2. Policy Enforcement Engine (`standard-read-only-v1`)

The FORGE Policy Engine strictly enforces structural safety before execution:

1. **Read-Only Evidence Access**: Forensic evidence sources can only be read; write/modify access to evidence files is physically prevented.
2. **Explicit Capability Declarations**: Scripts must explicitly declare required capabilities in `REQUIRE CAPABILITIES [...]`. Undeclared capability usage triggers immediate policy block.
3. **Prohibited Capability Denials**: Requests for prohibited capabilities (`WRITE_EVIDENCE`, `EXECUTE_PROCESS`, `DISABLE_SECURITY_CONTROL`, `LOAD_DRIVER`, etc.) are blocked at policy check, generating a `POLICY_DENIED` audit record without running the script.
4. **Directory Sandbox Boundaries**: Path inputs are constrained to `./datasets/`, `./exports/`, and `./reports/`. Path traversal (`../`) outside the sandbox is rejected.
5. **Immutable Hash-Chained Audit Log**: Every validation, policy check, execution, and export action is appended to a cryptographic hash chain (`prev_audit_hash`, `audit_hash`).
