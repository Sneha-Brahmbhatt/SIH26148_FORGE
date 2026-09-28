import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Navigation } from './components/Navigation';
import { SafetyBanner } from './components/SafetyBanner';

import { DashboardPage } from './pages/DashboardPage';
import { CaseManagementPage } from './pages/CaseManagementPage';
import { ScriptEditorPage } from './pages/ScriptEditorPage';
import { ValidationPipelinePage } from './pages/ValidationPipelinePage';
import { ExecutionPage } from './pages/ExecutionPage';
import { EvidencePage } from './pages/EvidencePage';
import { ComputerForensicsPage } from './pages/ComputerForensicsPage';
import { NetworkForensicsPage } from './pages/NetworkForensicsPage';
import { TimelinePage } from './pages/TimelinePage';
import { FindingsPage } from './pages/FindingsPage';
import { ChainOfCustodyPage } from './pages/ChainOfCustodyPage';
import { ReportsPage } from './pages/ReportsPage';
import { AuditLogsPage } from './pages/AuditLogsPage';
import { LanguageReferencePage } from './pages/LanguageReferencePage';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden font-sans">
        {/* Sidebar Navigation */}
        <Navigation />

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col h-screen overflow-y-auto">
          {/* Top Safety Banner */}
          <SafetyBanner />

          {/* Page Routes */}
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/cases" element={<CaseManagementPage />} />
              <Route path="/editor" element={<ScriptEditorPage />} />
              <Route path="/validation" element={<ValidationPipelinePage />} />
              <Route path="/execution" element={<ExecutionPage />} />
              <Route path="/evidence" element={<EvidencePage />} />
              <Route path="/computer" element={<ComputerForensicsPage />} />
              <Route path="/network" element={<NetworkForensicsPage />} />
              <Route path="/timeline" element={<TimelinePage />} />
              <Route path="/findings" element={<FindingsPage />} />
              <Route path="/chain-of-custody" element={<ChainOfCustodyPage />} />
              <Route path="/reports" element={<ReportsPage />} />
              <Route path="/audit" element={<AuditLogsPage />} />
              <Route path="/reference" element={<LanguageReferencePage />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
};

export default App;
