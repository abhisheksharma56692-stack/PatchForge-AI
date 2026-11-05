import React, { useState } from 'react';
import { WebSocketProvider } from './context/WebSocketContext';
import { VulnerabilityProvider } from './context/VulnerabilityContext';
import { AudioProvider, useAudio } from './context/AudioContext';
import { Navbar } from './components/layout/Navbar';
import { Sidebar } from './components/layout/Sidebar';
import { Footer } from './components/layout/Footer';
import { GhostParticles } from './components/domain/GhostParticles';

import HauntedHome from './pages/HauntedHome';
import VulnCrypt from './pages/VulnCrypt';
import PatchWorkbench from './pages/PatchWorkbench';
import Graveyard from './pages/Graveyard';
import SandboxDungeon from './pages/SandboxDungeon';
import HauntedAnalytics from './pages/HauntedAnalytics';

function DashboardContent() {
  const [activeTab, setActiveTab] = useState('home');
  const { isPlayingAmbient, toggleAmbient } = useAudio();

  const getPageTitle = (tab) => {
    switch (tab) {
      case 'home':
        return 'Haunted Command Center';
      case 'crypt':
        return 'Vulnerability Crypt & Taint Slices';
      case 'workbench':
        return 'Multi-Agent Patch Forge Workbench';
      case 'graveyard':
        return 'Vulnerability Graveyard (R.I.P.)';
      case 'dungeon':
        return 'Hermetic Sandbox Isolation Chamber';
      case 'analytics':
        return 'Cyber-Gothic Telemetry Analytics';
      default:
        return 'Operations Dashboard';
    }
  };

  const renderActivePage = () => {
    switch (activeTab) {
      case 'home':
        return <HauntedHome onNavigateToWorkbench={() => setActiveTab('workbench')} />;
      case 'crypt':
        return <VulnCrypt onNavigateToWorkbench={() => setActiveTab('workbench')} />;
      case 'workbench':
        return <PatchWorkbench />;
      case 'graveyard':
        return <Graveyard />;
      case 'dungeon':
        return <SandboxDungeon />;
      case 'analytics':
        return <HauntedAnalytics />;
      default:
        return <HauntedHome onNavigateToWorkbench={() => setActiveTab('workbench')} />;
    }
  };

  return (
    <div className="relative flex h-screen w-screen overflow-hidden bg-midnightBlack text-boneWhite font-body">
      {/* Background cobweb texture & ambient floating spirits */}
      <div
        className="absolute inset-0 pointer-events-none opacity-20 z-0 bg-repeat"
        style={{ backgroundImage: `url('/assets/textures/cobweb-corner.svg')` }}
      />
      <GhostParticles count={16} />

      {/* Navigation Sidebar */}
      <Sidebar activeTab={activeTab} onSelectTab={setActiveTab} />

      {/* Main Operations Frame */}
      <div className="flex-1 flex flex-col h-full overflow-hidden relative z-10">
        {/* Top Operational Status Navbar */}
        <Navbar
          activePageTitle={getPageTitle(activeTab)}
          isAudioPlaying={isPlayingAmbient}
          onToggleAudio={toggleAmbient}
        />

        {/* Scrollable Viewport */}
        <main className="flex-1 overflow-y-auto p-6 sm:p-8 scrollbar-thin">
          {renderActivePage()}
        </main>

        {/* Bottom GPG & Version Footer */}
        <Footer />
      </div>
    </div>
  );
}

export default function App() {
  return (
    <AudioProvider>
      <VulnerabilityProvider>
        <WebSocketProvider>
          <DashboardContent />
        </WebSocketProvider>
      </VulnerabilityProvider>
    </AudioProvider>
  );
}
