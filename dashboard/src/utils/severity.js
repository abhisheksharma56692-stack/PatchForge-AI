// CWE & Severity mapping to Skull counts and theme colors

export const getSkullCount = (severity = 'MEDIUM', cweId = '') => {
  const sev = String(severity).toUpperCase();
  if (sev === 'CRITICAL' || cweId.includes('CWE-89') || cweId.includes('CWE-78')) return 5;
  if (sev === 'HIGH' || cweId.includes('CWE-22') || cweId.includes('CWE-787')) return 4;
  if (sev === 'MEDIUM' || cweId.includes('CWE-79')) return 3;
  if (sev === 'LOW') return 2;
  return 1;
};

export const getSeverityLabel = (skullCount) => {
  switch (skullCount) {
    case 5:
      return 'Catastrophic Curse (Critical)';
    case 4:
      return 'Deadly Hex (High)';
    case 3:
      return 'Spooky Jinx (Medium)';
    case 2:
      return 'Minor Phantom (Low)';
    default:
      return 'Whispering Spirit (Info)';
  }
};

export const getSeverityBadgeVariant = (skullCount) => {
  if (skullCount >= 5) return 'critical';
  if (skullCount === 4) return 'high';
  if (skullCount === 3) return 'medium';
  return 'low';
};

