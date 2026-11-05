import React, { useState, useEffect } from 'react';
import { Cloud, Radio, Volume2, VolumeX, ShieldCheck, Clock, Download } from 'lucide-react';

export const Navbar = ({ activePageTitle, isAudioPlaying, onToggleAudio }) => {
  const [currentTime, setCurrentTime] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date().toLocaleTimeString()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="h-14 border-b border-coffinBorder/60 bg-coffinDark/80 backdrop-blur-md px-6 flex items-center justify-between z-20">
      {/* Left: Active Section Indicator */}
      <div className="flex items-center gap-3">
        <span className="w-2.5 h-2.5 rounded-full bg-pumpkinOrange animate-ping" />
        <h1 className="font-mono text-sm font-semibold text-boneWhite tracking-wider uppercase">
          {activePageTitle}
        </h1>
      </div>

      {/* Right: Operational Status Indicators */}
      <div className="flex items-center gap-4 text-xs font-mono">
        {/* Download PPTX Deck */}
        <a
          href="/PatchForge_AI_Pitch_Deck.pptx"
          download="PatchForge_AI_Pitch_Deck.pptx"
          className="flex items-center gap-1.5 px-3 py-1 rounded bg-pumpkinOrange/20 hover:bg-pumpkinOrange/30 border border-pumpkinOrange/60 text-pumpkinOrange hover:text-white transition-all shadow-sm font-semibold"
          title="Download Presentation Pitch Deck (.pptx)"
        >
          <Download className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Pitch Deck (PPTX)</span>
        </a>

        {/* AWS Cloud Status */}
        <div className="hidden lg:flex items-center gap-1.5 px-2.5 py-1 rounded bg-deepGrave border border-coffinBorder text-boneWhite">
          <Cloud className="w-3.5 h-3.5 text-pumpkinOrange" />
          <span>AWS Active</span>
        </div>

        {/* WebSocket Telemetry Status */}
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-deepGrave border border-ghostGreen/30 text-ghostGreen">
          <Radio className="w-3.5 h-3.5 animate-pulse" />
          <span className="hidden md:inline">Telemetry:</span>
          <span>ONLINE</span>
        </div>

        {/* GPG Signature Badge */}
        <div className="hidden lg:flex items-center gap-1.5 px-2.5 py-1 rounded bg-deepGrave border border-coffinBorder text-cryptGray">
          <ShieldCheck className="w-3.5 h-3.5 text-cauldronGold" />
          <span>GPG: 0xDEADBEEF</span>
        </div>

        {/* Live Clock */}
        <div className="hidden md:flex items-center gap-1.5 text-cryptGray">
          <Clock className="w-3.5 h-3.5" />
          <span>{currentTime}</span>
        </div>

        {/* Ambient Audio Toggle */}
        <button
          onClick={onToggleAudio}
          className="p-1.5 rounded-lg border border-coffinBorder bg-coffinPurple/40 text-cryptGray hover:text-pumpkinOrange hover:border-pumpkinOrange transition-colors"
          title={isAudioPlaying ? 'Mute Ambient Cyber-Gothic Soundscape' : 'Play Ambient Soundscape'}
        >
          {isAudioPlaying ? <Volume2 className="w-4 h-4 text-pumpkinOrange animate-pulse" /> : <VolumeX className="w-4 h-4" />}
        </button>
      </div>
    </header>
  );
};

export default Navbar;

