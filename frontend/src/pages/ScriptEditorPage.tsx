import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../api/client';
import { Code2, CheckCircle2, Play, FileCode, ShieldAlert, Sparkles } from 'lucide-react';

const SCRIPT_TEMPLATES: Record<string, string> = {
  'demo_full_analysis.forge': `CASE "CASE-001"

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
system = SYSTEM_CONFIG()

files = FILE_LIST("./datasets/computer/files")
file_metadata = FILE_METADATA(files)
file_hashes = HASH_FILES(files, "SHA256")

events_system = EVENT_LOGS("System")
events_security = EVENT_LOGS("Security")

pcap = PCAP_LOAD("./datasets/network/sample.pcap")
connections = NETWORK_CONNECTIONS(pcap)
dns = DNS_ACTIVITY(pcap)
protocol_stats = PROTOCOL_STATS(pcap)
flow_summary = FLOW_SUMMARY(pcap)

timeline = BUILD_TIMELINE([
    host_info,
    processes,
    services,
    file_metadata,
    events_system,
    events_security,
    connections,
    dns
])

findings = ANALYZE_FINDINGS(timeline, file_hashes, dns)

EXPORT_EVIDENCE(file_hashes, "./exports/file_hashes.json")
EXPORT_REPORT(findings, "./reports/CASE-001-report", "json")
EXPORT_REPORT(findings, "./reports/CASE-001-report", "csv")
EXPORT_REPORT(findings, "./reports/CASE-001-report", "html")
`,

  'demo_policy_blocked.forge': `CASE "CASE-BAD"

REQUIRE ANALYST "unauthorized@org.example"
REQUIRE POLICY "standard-read-only-v1"
REQUIRE CAPABILITIES [
    WRITE_EVIDENCE,
    EXECUTE_PROCESS,
    DISABLE_SECURITY_CONTROL
]

EXECUTE_PROCESS("cmd.exe")
WRITE_EVIDENCE("./evidence/disk.E01", "modified")
`
};

export const ScriptEditorPage: React.FC = () => {
  const navigate = useNavigate();
  const [selectedTemplate, setSelectedTemplate] = useState('demo_full_analysis.forge');
  const [sourceCode, setSourceCode] = useState(SCRIPT_TEMPLATES['demo_full_analysis.forge']);
  const [validating, setValidating] = useState(false);
  const [executing, setExecuting] = useState(false);
  const [lastValidation, setLastValidation] = useState<any>(null);

  const handleTemplateChange = (tmplName: string) => {
    setSelectedTemplate(tmplName);
    setSourceCode(SCRIPT_TEMPLATES[tmplName] || '');
    setLastValidation(null);
  };

  const handleValidate = async () => {
    setValidating(true);
    try {
      const res = await apiClient.validateScript(sourceCode);
      setLastValidation(res);
      navigate('/validation', { state: { validationResult: res } });
    } catch (err) {
      console.error(err);
    } finally {
      setValidating(false);
    }
  };

  const handleExecute = async () => {
    setExecuting(true);
    try {
      const res = await apiClient.executeScript(sourceCode);
      navigate('/execution', { state: { executionResult: res } });
    } catch (err) {
      console.error(err);
    } finally {
      setExecuting(false);
    }
  };

  const lineCount = sourceCode.split('\n').length;
  const lineNumbers = Array.from({ length: lineCount }, (_, i) => i + 1);

  return (
    <div className="p-6 space-y-6">
      {/* Top Controls Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-xl font-bold font-mono text-slate-100 flex items-center space-x-2">
            <Code2 className="w-5 h-5 text-cyan-400" />
            <span>FORGE Forensic Script Editor</span>
          </h1>
          <p className="text-xs font-mono text-slate-400 mt-1">
            Author and inspect forensic analysis DSL scripts in a governed, capability-checked environment.
          </p>
        </div>

        {/* Action Controls */}
        <div className="flex items-center space-x-3">
          {/* Template Selector */}
          <div className="flex items-center space-x-2 bg-slate-900 border border-slate-800 rounded px-2 py-1">
            <FileCode className="w-4 h-4 text-slate-400" />
            <select
              value={selectedTemplate}
              onChange={(e) => handleTemplateChange(e.target.value)}
              className="bg-transparent text-xs font-mono text-slate-200 focus:outline-none"
            >
              <option value="demo_full_analysis.forge">demo_full_analysis.forge (VALID)</option>
              <option value="demo_policy_blocked.forge">demo_policy_blocked.forge (PROHIBITED)</option>
            </select>
          </div>

          <button
            onClick={handleValidate}
            disabled={validating}
            className="flex items-center space-x-1.5 bg-slate-800 hover:bg-slate-700 text-cyan-400 font-mono text-xs font-semibold px-4 py-2 rounded border border-cyan-500/30 transition disabled:opacity-50"
          >
            <CheckCircle2 className="w-4 h-4" />
            <span>{validating ? 'VALIDATING...' : 'VALIDATE SCRIPT'}</span>
          </button>

          <button
            onClick={handleExecute}
            disabled={executing}
            className="flex items-center space-x-1.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-mono text-xs font-bold px-5 py-2 rounded shadow transition disabled:opacity-50"
          >
            <Play className="w-4 h-4 fill-current" />
            <span>{executing ? 'RUNNING...' : 'EXECUTE ANALYSIS'}</span>
          </button>
        </div>
      </div>

      {/* Editor Container */}
      <div className="bg-slate-950 border border-slate-800 rounded-lg overflow-hidden shadow-xl flex flex-col h-[520px]">
        {/* Editor Titlebar */}
        <div className="bg-slate-900 px-4 py-2 border-b border-slate-800 flex items-center justify-between text-xs font-mono">
          <div className="flex items-center space-x-2 text-slate-300">
            <Sparkles className="w-4 h-4 text-purple-400" />
            <span className="font-bold">{selectedTemplate}</span>
            <span className="text-[10px] text-slate-500">FORGE DSL v1.0</span>
          </div>
          <span className="text-[10px] text-slate-500">
            POLICY: standard-read-only-v1
          </span>
        </div>

        {/* Text Area with Line Numbers */}
        <div className="flex-1 flex overflow-hidden">
          {/* Line Numbers Sidebar */}
          <div className="bg-slate-900/60 text-slate-600 font-mono text-xs p-3 select-none text-right border-r border-slate-800/60 min-w-[40px]">
            {lineNumbers.map((num) => (
              <div key={num}>{num}</div>
            ))}
          </div>

          {/* Textarea Code Input */}
          <textarea
            value={sourceCode}
            onChange={(e) => setSourceCode(e.target.value)}
            spellCheck={false}
            className="flex-1 bg-slate-950 text-slate-100 font-mono text-xs p-3 leading-relaxed focus:outline-none resize-none overflow-y-auto selection:bg-cyan-500 selection:text-slate-950"
          />
        </div>
      </div>
    </div>
  );
};
