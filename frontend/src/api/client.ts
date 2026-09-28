import axios from 'axios';
import {
  Case, ScriptValidationResponse, Execution, EvidenceItem,
  TimelineEvent, Finding, AuditLogItem, ReportItem
} from '../types';

const API_BASE = '/api/v1';

export const apiClient = {
  getHealth: async () => {
    const res = await axios.get(`${API_BASE}/health`);
    return res.data;
  },

  getCases: async (): Promise<Case[]> => {
    const res = await axios.get(`${API_BASE}/cases`);
    return res.data;
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
    const res = await axios.get(`${API_BASE}/executions`);
    return res.data;
  },

  getExecutionDetails: async (id: string): Promise<Execution> => {
    const res = await axios.get(`${API_BASE}/executions/${id}`);
    return res.data;
  },

  getEvidence: async (): Promise<EvidenceItem[]> => {
    const res = await axios.get(`${API_BASE}/evidence`);
    return res.data;
  },

  getTimeline: async (): Promise<TimelineEvent[]> => {
    const res = await axios.get(`${API_BASE}/timeline`);
    return res.data;
  },

  getFindings: async (): Promise<Finding[]> => {
    const res = await axios.get(`${API_BASE}/findings`);
    return res.data;
  },

  getAuditLogs: async (): Promise<AuditLogItem[]> => {
    const res = await axios.get(`${API_BASE}/audit`);
    return res.data;
  },

  getChainOfCustody: async (case_id = 'CASE-001') => {
    const res = await axios.get(`${API_BASE}/chain-of-custody/${case_id}`);
    return res.data;
  },

  getReports: async (): Promise<ReportItem[]> => {
    const res = await axios.get(`${API_BASE}/reports`);
    return res.data;
  },

  getLanguageReference: async () => {
    const res = await axios.get(`${API_BASE}/language/reference`);
    return res.data;
  },

  // Forensics sub-system details
  getHosts: async () => (await axios.get(`${API_BASE}/hosts`)).data,
  getProcesses: async () => (await axios.get(`${API_BASE}/processes`)).data,
  getServices: async () => (await axios.get(`${API_BASE}/services`)).data,
  getFiles: async () => (await axios.get(`${API_BASE}/files`)).data,
  getEvents: async (source = 'System') => (await axios.get(`${API_BASE}/events?source=${source}`)).data,
  getNetworkFlows: async () => (await axios.get(`${API_BASE}/network/flows`)).data,
  getNetworkDNS: async () => (await axios.get(`${API_BASE}/network/dns`)).data,
  getNetworkProtocols: async () => (await axios.get(`${API_BASE}/network/protocols`)).data,
};
