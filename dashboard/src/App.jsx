import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import GhostParticles from './components/GhostParticles';
import HauntedHome from './pages/HauntedHome';
import VulnCrypt from './pages/VulnCrypt';
import PatchWorkbench from './pages/PatchWorkbench';
import Graveyard from './pages/Graveyard';
import SandboxDungeon from './pages/SandboxDungeon';
import HauntedAnalytics from './pages/HauntedAnalytics';

export default function App() {
  const [activeTab, setActiveTab] = useState('home');

  const renderPage = () => {
    switch (activeTab) {
      case 'home':
        return <HauntedHome />;
      case 'crypt':
        return <VulnCrypt />;
      case 'workbench':
        return <PatchWorkbench />;
      case 'graveyard':
        return <Graveyard />;
      case 'dungeon':
        return <SandboxDungeon />;
      case 'analytics':
        return <HauntedAnalytics />;
      default:
        return <HauntedHome />;
    }
  };

  return (
    <div className="relative flex h-screen w-screen overflow-hidden bg-midnightBlack text-boneWhite">
      {/* Background cobweb texture & ghost particles */}
      <div
        className="absolute inset-0 pointer-events-none opacity-20"
        style={{ backgroundImage: `url('/assets/cobweb-texture.svg')` }}
      />
      <GhostParticles />

      {/* Navigation Sidebar */}
      <Sidebar activeTab={activeTab} onSelectTab={setActiveTab} />

      {/* Main Operations Content Pane */}
      <main className="flex-1 overflow-y-auto p-8 relative z-10">
        {renderPage()}
      </main>
    </div>
  );
}

