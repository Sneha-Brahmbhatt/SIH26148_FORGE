"""
FORGE Evidence, Provenance & Immutable Audit Log Manager
Enforces SHA-256 evidence hashing, provenance tracking, and append-only hash-chained audit logging.
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

class EvidenceManager:
    def __init__(self):
        self.evidence_records: List[Dict[str, Any]] = []
        self.provenance_records: List[Dict[str, Any]] = []
        self.audit_records: List[Dict[str, Any]] = []
        self.last_audit_hash: str = "0000000000000000000000000000000000000000000000000000000000000000"

    def record_audit_event(
        self,
        case_id: str,
        execution_id: str,
        actor: str,
        action: str,
        object_type: str,
        object_id: str,
        result: str,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        audit_id = f"AUD-{len(self.audit_records) + 1:06d}"
        now_iso = datetime.now(timezone.utc).isoformat()
        details_dict = details or {}

        record_data = {
            "audit_id": audit_id,
            "case_id": case_id,
            "execution_id": execution_id,
            "actor": actor,
            "action": action,
            "object_type": object_type,
            "object_id": object_id,
            "result": result,
            "timestamp_utc": now_iso,
            "details_json": json.dumps(details_dict, sort_keys=True),
            "prev_audit_hash": self.last_audit_hash
        }

        # Calculate canonical SHA-256 hash for hash chain
        canonical_str = json.dumps(record_data, sort_keys=True)
        audit_hash = hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()
        
        record_data["audit_hash"] = audit_hash
        self.last_audit_hash = audit_hash
        self.audit_records.append(record_data)

        return record_data

    def create_evidence_record(
        self,
        case_id: str,
        execution_id: str,
        script_id: str,
        script_version: str,
        source: str,
        collector: str,
        evidence_type: str,
        data: Any,
        provenance_id: str,
        synthetic: bool = True
    ) -> Dict[str, Any]:
        evd_id = f"EVD-{len(self.evidence_records) + 1:06d}"
        now_iso = datetime.now(timezone.utc).isoformat()

        serialized_data = json.dumps(data, sort_keys=True)
        sha256_val = hashlib.sha256(serialized_data.encode("utf-8")).hexdigest()

        rec_count = len(data) if isinstance(data, list) else 1

        evd_record = {
            "evidence_id": evd_id,
            "case_id": case_id,
            "execution_id": execution_id,
            "script_id": script_id,
            "script_version": script_version,
            "source": source,
            "collector": collector,
            "evidence_type": evidence_type,
            "collection_status": "SUCCESS",
            "collected_at_utc": now_iso,
            "sha256": sha256_val,
            "hash_algorithm": "SHA-256",
            "record_count": rec_count,
            "synthetic": synthetic,
            "provenance_id": provenance_id
        }

        self.evidence_records.append(evd_record)
        return evd_record

    def create_provenance_record(
        self,
        case_id: str,
        execution_id: str,
        analyst_id: str,
        script_id: str,
        script_version: str,
        script_source: str,
        policy_version: str = "standard-read-only-v1",
        dataset_version: str = "demo-dataset-v1"
    ) -> Dict[str, Any]:
        prv_id = f"PRV-{len(self.provenance_records) + 1:06d}"
        now_iso = datetime.now(timezone.utc).isoformat()
        script_sha = hashlib.sha256(script_source.encode("utf-8")).hexdigest()

        prv_record = {
            "provenance_id": prv_id,
            "case_id": case_id,
            "execution_id": execution_id,
            "analyst_id": analyst_id,
            "script_id": script_id,
            "script_version": script_version,
            "script_sha256": script_sha,
            "policy_version": policy_version,
            "runtime_version": "forge-0.1.0",
            "dataset_version": dataset_version,
            "evidence_ids": [],
            "input_hashes": [],
            "output_hashes": [],
            "started_at_utc": now_iso,
            "completed_at_utc": None,
            "parameters": {
                "hash_algorithm": "SHA256",
                "timezone": "UTC+05:30"
            }
        }

        self.provenance_records.append(prv_record)
        return prv_record

    def verify_audit_chain(self) -> Dict[str, Any]:
        """
        Verifies the integrity of the hash-chained audit trail.
        """
        valid = True
        broken_id = None
        expected_prev = "0000000000000000000000000000000000000000000000000000000000000000"

        for rec in self.audit_records:
            if rec["prev_audit_hash"] != expected_prev:
                valid = False
                broken_id = rec["audit_id"]
                break

            # Recompute hash
            check_dict = {k: v for k, v in rec.items() if k != "audit_hash"}
            canonical_str = json.dumps(check_dict, sort_keys=True)
            recomputed = hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()

            if recomputed != rec["audit_hash"]:
                valid = False
                broken_id = rec["audit_id"]
                break

            expected_prev = rec["audit_hash"]

        return {
            "chain_valid": valid,
            "total_records": len(self.audit_records),
            "broken_record_id": broken_id,
            "head_hash": self.last_audit_hash
        }
