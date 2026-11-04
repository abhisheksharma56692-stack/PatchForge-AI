import React from 'react';

const NAV_ITEMS = [
  { id: 'home', label: 'Haunted Home', icon: '🏚️' },
  { id: 'crypt', label: 'Vuln Crypt', icon: '💀' },
  { id: 'workbench', label: 'Patch Workbench', icon: '🔬' },
  { id: 'graveyard', label: 'Graveyard', icon: '⚰️' },
  { id: 'dungeon', label: 'Sandbox Dungeon', icon: '🧪' },
  { id: 'analytics', label: 'Haunted Analytics', icon: '📊' },
];

export default function Sidebar({ activeTab, onSelectTab }) {
  return (
    <aside className="w-64 bg-deepGrave border-r border-cobwebGray/60 flex flex-col justify-between p-4 z-20">
      <div>
        {/* Brand Header */}
        <div className="flex items-center space-x-3 mb-8 px-2">
          <span className="text-3xl animate-bounce">🎃</span>
          <div>
            <h1 className="font-creepster text-2xl tracking-wider text-pumpkinOrange drop-shadow">
              PatchForge AI
            </h1>
            <p className="text-[10px] font-mono text-boneWhite/50 uppercase tracking-widest">
              Autonomous Remediation
            </p>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="space-y-1">
          {NAV_ITEMS.map((item) => {
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onSelectTab(item.id)}
                className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-mono transition-all duration-200 text-left ${
                  isActive
                    ? 'bg-coffinPurple text-pumpkinOrange border-l-4 border-pumpkinOrange shadow-pumpkin-glow font-bold'
                    : 'text-boneWhite/70 hover:bg-coffinPurple/50 hover:text-boneWhite'
                }`}
              >
                <span className="text-lg">{item.icon}</span>
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer Info */}
      <div className="pt-4 border-t border-cobwebGray/40 text-[11px] font-mono text-boneWhite/40 px-2 space-y-1">
        <div className="flex items-center justify-between">
          <span>Engine State:</span>
          <span className="text-ghostGreen font-bold">ACTIVE</span>
        </div>
        <div className="flex items-center justify-between">
          <span>AWS Bedrock:</span>
          <span className="text-pumpkinOrange font-bold">ONLINE</span>
        </div>
        <div className="text-center pt-2 text-[10px] text-boneWhite/30">
          v1.0.0 • Halloween Edition
        </div>
      </div>
    </aside>
  );
}

