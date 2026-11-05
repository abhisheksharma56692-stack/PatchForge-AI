import React from 'react';
import {
  Skull,
  Activity,
  Flame,
  Archive,
  Terminal,
  BarChart3,
  Sparkles,
} from 'lucide-react';

export const Sidebar = ({ activeTab, onSelectTab }) => {
  const navItems = [
    { id: 'home', label: 'Haunted Home', icon: Flame, badge: 'Live' },
    { id: 'crypt', label: 'Vuln Crypt', icon: Skull, badge: '4' },
    { id: 'workbench', label: 'Patch Workbench', icon: Activity, badge: 'Agent' },
    { id: 'graveyard', label: 'Graveyard (R.I.P.)', icon: Archive, badge: '8' },
    { id: 'dungeon', label: 'Sandbox Dungeon', icon: Terminal, badge: 'Air-Gap' },
    { id: 'analytics', label: 'Haunted Analytics', icon: BarChart3 },
  ];

  return (
    <aside className="w-64 border-r border-coffinBorder/60 bg-[#0d0714]/95 backdrop-blur-md flex flex-col justify-between p-4 z-20 select-none">
      <div>
        {/* Brand Header */}
        <div className="flex items-center gap-3 px-2 py-3 mb-6 border-b border-coffinBorder/50">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-pumpkinOrange to-bloodRed flex items-center justify-center shadow-pumpkin">
            <span className="text-xl">🎃</span>
          </div>
          <div>
            <div className="font-creepster text-2xl text-pumpkinOrange tracking-wide leading-none">
              PatchForge AI
            </div>
            <div className="text-[10px] font-mono text-cryptGray tracking-wider uppercase mt-1">
              DevSecOps Remediation
            </div>
          </div>
        </div>

        {/* Navigation List */}
        <nav className="space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onSelectTab(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl font-mono text-xs transition-all duration-200 ${
                  isActive
                    ? 'bg-gradient-to-r from-pumpkinOrange/20 to-coffinPurple text-pumpkinOrange border border-pumpkinOrange/60 shadow-[0_0_15px_rgba(255,106,0,0.2)]'
                    : 'text-cryptGray hover:text-boneWhite hover:bg-coffinPurple/40 border border-transparent'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-4 h-4 ${isActive ? 'text-pumpkinOrange' : 'text-cryptGray'}`} />
                  <span className="font-medium tracking-wide">{item.label}</span>
                </div>
                {item.badge && (
                  <span
                    className={`px-1.5 py-0.5 rounded text-[10px] font-mono ${
                      isActive
                        ? 'bg-pumpkinOrange text-midnightBlack font-bold'
                        : 'bg-coffinBorder/80 text-cryptGray'
                    }`}
                  >
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Bottom Engine Specs Card */}
      <div className="p-3 rounded-xl bg-deepGrave border border-coffinBorder/60 text-xs font-mono">
        <div className="flex items-center gap-2 text-ghostGreen mb-1">
          <Sparkles className="w-3.5 h-3.5" />
          <span className="font-semibold">Z3 SMT Invariant Prover</span>
        </div>
        <p className="text-[11px] text-cryptGray leading-relaxed">
          First-Order Logic safety bounds mathematically verified before git commit.
        </p>
      </div>
    </aside>
  );
};

export default Sidebar;

