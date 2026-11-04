import React, { useEffect, useState } from 'react';
import SkullRating from '../components/SkullRating';
import { fetchVulnerabilities } from '../services/api';

export default function VulnCrypt() {
  const [vulns, setVulns] = useState([]);
  const [filterCwe, setFilterCwe] = useState('ALL');

  useEffect(() => {
    fetchVulnerabilities().then(setVulns);
  }, []);

  const filtered = filterCwe === 'ALL'
    ? vulns
    : vulns.filter((v) => v.cwe_id.includes(filterCwe));

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="font-creepster text-3xl text-boneWhite tracking-wide">
            💀 The Vulnerability Crypt
          </h2>
          <p className="text-xs font-mono text-boneWhite/60 mt-1">
            Active security flaws detected by SARIF static analyzers waiting for autonomous remediation.
          </p>
        </div>

        {/* Filter */}
        <div className="flex items-center space-x-2">
          <span className="text-xs font-mono text-boneWhite/50">Filter CWE:</span>
          <select
            value={filterCwe}
            onChange={(e) => setFilterCwe(e.target.value)}
            className="bg-deepGrave border border-cobwebGray/80 rounded-lg px-3 py-1.5 text-xs font-mono text-pumpkinOrange focus:outline-none focus:border-pumpkinOrange"
          >
            <option value="ALL">All Flaws</option>
            <option value="CWE-89">CWE-89 (SQLi)</option>
            <option value="CWE-22">CWE-22 (Path Traversal)</option>
            <option value="CWE-79">CWE-79 (XSS)</option>
          </select>
        </div>
      </div>

      {/* Crypt Table */}
      <div className="border border-cobwebGray/60 rounded-xl overflow-hidden bg-deepGrave">
        <table className="w-full text-left font-mono text-xs">
          <thead className="bg-coffinPurple/70 text-boneWhite/60 uppercase tracking-wider border-b border-cobwebGray/60">
            <tr>
              <th className="p-3.5">CWE / Rule</th>
              <th className="p-3.5">Title & Description</th>
              <th className="p-3.5">Location</th>
              <th className="p-3.5">Skull Severity</th>
              <th className="p-3.5">Scanner</th>
              <th className="p-3.5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-cobwebGray/30 text-boneWhite/90">
            {filtered.map((item) => (
              <tr key={item.finding_id} className="hover:bg-coffinPurple/30 transition-colors">
                <td className="p-3.5 font-bold text-pumpkinOrange">
                  {item.cwe_id}
                </td>
                <td className="p-3.5 max-w-xs truncate" title={item.title}>
                  {item.title}
                </td>
                <td className="p-3.5 text-boneWhite/70">
                  <span className="text-pumpkinGlow">{item.file_path}</span>:{item.start_line}
                </td>
                <td className="p-3.5">
                  <SkullRating count={item.skull_rating} />
                </td>
                <td className="p-3.5 uppercase text-boneWhite/60">
                  {item.scanner}
                </td>
                <td className="p-3.5">
                  <span className="px-2 py-0.5 rounded-full text-[10px] bg-pumpkinOrange/20 text-pumpkinOrange border border-pumpkinOrange/50">
                    {item.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

