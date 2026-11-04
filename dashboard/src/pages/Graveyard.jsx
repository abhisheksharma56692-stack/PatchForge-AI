import React, { useEffect, useState } from 'react';
import TombstoneCard from '../components/TombstoneCard';
import { fetchGraveyard } from '../services/api';

export default function Graveyard() {
  const [tombstones, setTombstones] = useState([]);

  useEffect(() => {
    fetchGraveyard().then(setTombstones);
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="font-creepster text-3xl text-boneWhite tracking-wide">
            ⚰️ The Vulnerability Graveyard
          </h2>
          <p className="text-xs font-mono text-boneWhite/60 mt-1">
            Historical resting place of all vulnerabilities defeated, formally proved, and verified by PatchForge AI.
          </p>
        </div>
        <div className="text-xs font-mono px-3 py-1 bg-ghostGreen/10 border border-ghostGreen/40 text-ghostGreen rounded-full">
          👻 {tombstones.length} Neutralized Threats Resting In Peace
        </div>
      </div>

      {/* Tombstones Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {tombstones.map((record) => (
          <TombstoneCard key={record.run_id} record={record} />
        ))}
      </div>
    </div>
  );
}

