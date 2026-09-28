import axios from 'axios';
import {
  Case, ScriptValidationResponse, Execution, EvidenceItem,
  TimelineEvent, Finding, AuditLogItem, ReportItem
} from '../types';

const API_BASE = (((import.meta as any).env?.VITE_FORENSIC_API_URL as string) || '').replace(/\/$/, '') + '/api/v1';

const safeArray = <T>(data: any): T[] => {
  return Array.isArray(data) ? data : [];
};

export const apiClient = {
  getHealth: async () => {
    try {
      const res = await axios.get(`${API_BASE}/health`);
      return typeof res.data === 'object' && res.data ? res.data : { status: 'OFFLINE' };
    } catch {
      return { status: 'OFFLINE' };
    }
  },

  getCases: async (): Promise<Case[]> => {
    try {
      const res = await axios.get(`${API_BASE}/cases`);
      return safeArray<Case>(res.data);
    } catch {
      return [];
    }
  },

  createCase: async (title: string, description: string): Promise<Case> => {
    const res = await axios.post(`${API_BASE}/cases`, {
      title,
      description,
      analyst_id: 'investigator@org.example'
    });
    return res.data;
  },

  validateScript: async (source_code: string): Promise<ScriptValidationResponse> => {
    const res = await axios.post(`${API_BASE}/scripts/validate`, {
      source_code,
      policy_name: 'standard-read-only-v1'
    });
    return res.data;
  },

  executeScript: async (source_code: string, script_id = 'SCR-001', case_id = 'CASE-001'): Promise<Execution> => {
    const res = await axios.post(`${API_BASE}/scripts/execute`, {
      script_id,
      source_code,
      case_id,
      analyst_id: 'investigator@org.example',
      policy_name: 'standard-read-only-v1'
    });
    return res.data;
  },

  runSIHDemo: async (): Promise<Execution> => {
    const res = await axios.post(`${API_BASE}/demo/run`);
    return res.data;
  },

  getExecutions: async (): Promise<any[]> => {
    try {
      const res = await axios.get(`${API_BASE}/executions`);
      return safeArray(res.data);
    } catch {
      return [];
    }
  },

  getExecutionDetails: async (id: string): Promise<Execution> => {
    const res = await axios.get(`${API_BASE}/executions/${id}`);
    return res.data;
  },

  getEvidence: async (): Promise<EvidenceItem[]> => {
    try {
      const res = await axios.get(`${API_BASE}/evidence`);
      return safeArray<EvidenceItem>(res.data);
    } catch {
      return [];
    }
  },

  getTimeline: async (): Promise<TimelineEvent[]> => {
    try {
      const res = await axios.get(`${API_BASE}/timeline`);
      return safeArray<TimelineEvent>(res.data);
    } catch {
      return [];
    }
  },

  getFindings: async (): Promise<Finding[]> => {
    try {
      const res = await axios.get(`${API_BASE}/findings`);
      return safeArray<Finding>(res.data);
    } catch {
      return [];
    }
  },

  getAuditLogs: async (): Promise<AuditLogItem[]> => {
    try {
      const res = await axios.get(`${API_BASE}/audit`);
      return safeArray<AuditLogItem>(res.data);
    } catch {
      return [];
    }
  },

  getChainOfCustody: async (case_id = 'CASE-001') => {
    try {
      const res = await axios.get(`${API_BASE}/chain-of-custody/${case_id}`);
      return typeof res.data === 'object' && res.data ? res.data : { chain_events: [], evidence_items: [] };
    } catch {
      return { chain_events: [], evidence_items: [] };
    }
  },

  getReports: async (): Promise<ReportItem[]> => {
    try {
      const res = await axios.get(`${API_BASE}/reports`);
      return safeArray<ReportItem>(res.data);
    } catch {
      return [];
    }
  },

  getLanguageReference: async () => {
    try {
      const res = await axios.get(`${API_BASE}/language/reference`);
      return res.data;
    } catch {
      return { commands: [], prohibited_capabilities: [] };
    }
  },

  // Forensics sub-system details
  getHosts: async () => {
    try {
      const res = await axios.get(`${API_BASE}/hosts`);
      return safeArray(res.data);
    } catch {
      return [];
    }
  },

  getProcesses: async () => {
    try {
      const res = await axios.get(`${API_BASE}/processes`);
      return safeArray(res.data);
    } catch {
      return [];
    }
  },

  getServices: async () => {
    try {
      const res = await axios.get(`${API_BASE}/services`);
      return safeArray(res.data);
    } catch {
      return [];
    }
  },

  getFiles: async () => {
    try {
      const res = await axios.get(`${API_BASE}/files`);
      return safeArray(res.data);
    } catch {
      return [];
    }
  },

  getEvents: async (source = 'System') => {
    try {
      const res = await axios.get(`${API_BASE}/events?source=${source}`);
      return safeArray(res.data);
    } catch {
      return [];
    }
  },

  getNetworkFlows: async () => {
    try {
      const res = await axios.get(`${API_BASE}/network/flows`);
      return safeArray(res.data);
    } catch {
      return [];
    }
  },

  getNetworkDNS: async () => {
    try {
      const res = await axios.get(`${API_BASE}/network/dns`);
      return safeArray(res.data);
    } catch {
      return [];
    }
  },

  getNetworkProtocols: async () => {
    try {
      const res = await axios.get(`${API_BASE}/network/protocols`);
      return safeArray(res.data);
    } catch {
      return [];
    }
  },
};
