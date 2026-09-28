export interface Case {
  case_id: string;
  title: string;
  description: string;
  status: string;
  analyst_id: string;
  created_at_utc: string;
  closed_at_utc?: string;
}

export interface ScriptValidationResponse {
  valid: boolean;
  lexer: {
    token_count: number;
    tokens: any[];
    error?: string;
  };
  parser: {
    ast: any;
    errors: string[];
  };
  semantic: {
    errors: any[];
    warnings: any[];
  };
  policy: {
    decision: 'APPROVED' | 'BLOCKED';
    policy_name: string;
    required_capabilities: string[];
    invoked_capabilities: string[];
    missing_capabilities: string[];
    denied_capabilities: string[];
    command_checks: any[];
    path_violations: string[];
    violations: string[];
  };
  script_sha256: string;
  ready_for_execution: boolean;
}

export interface Execution {
  execution_id: string;
  case_id: string;
  script_id: string;
  script_version: string;
  analyst_id: string;
  status: string;
  policy_decision: 'APPROVED' | 'BLOCKED';
  policy_result: any;
  started_at_utc: string;
  completed_at_utc?: string;
  duration_ms: number;
  evidence?: EvidenceItem[];
  timeline?: TimelineEvent[];
  findings?: Finding[];
  audit_summary?: {
    chain_valid: boolean;
    total_records: number;
    head_hash: string;
  };
  audit_logs?: AuditLogItem[];
  provenance?: any;
  error?: string;
}

export interface EvidenceItem {
  evidence_id: string;
  case_id: string;
  execution_id: string;
  script_id: string;
  script_version: string;
  source: string;
  collector: string;
  evidence_type: string;
  collection_status: string;
  collected_at_utc: string;
  sha256: string;
  hash_algorithm: string;
  record_count: number;
  synthetic: boolean;
  provenance_id: string;
}

export interface TimelineEvent {
  timeline_event_id: string;
  case_id: string;
  execution_id: string;
  timestamp_utc: string;
  event_type: 'FILE' | 'PROCESS' | 'NETWORK' | 'DNS' | 'EVENT_LOG' | 'SYSTEM' | 'BROWSER' | 'REGISTRY';
  source: string;
  title: string;
  description: string;
  evidence_id?: string;
  related_object?: string;
  severity: 'INFO' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  synthetic: boolean;
}

export interface Finding {
  finding_id: string;
  case_id: string;
  execution_id: string;
  severity: 'HIGH' | 'MEDIUM' | 'LOW' | 'INFO';
  category: string;
  timestamp_utc: string;
  title: string;
  description: string;
  observed_evidence: string;
  derived_analysis: string;
  analyst_interpretation_required: string;
  confidence: string;
  analysis_type: string;
  evidence_ids?: string[];
  related_artifacts?: string[];
}

export interface AuditLogItem {
  audit_id: string;
  case_id: string;
  execution_id: string;
  actor: string;
  action: string;
  object_type: string;
  object_id: string;
  result: string;
  timestamp_utc: string;
  details_json?: string;
  prev_audit_hash: string;
  audit_hash: string;
}

export interface ReportItem {
  report_id: string;
  filename: string;
  path: string;
  size_bytes: number;
  sha256: string;
  created_at_utc: string;
}

export interface DSLCommandReference {
  command: string;
  capability: string;
  purpose: string;
  syntax: string;
}
