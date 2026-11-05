import React, { createContext, useContext, useEffect, useState } from 'react';
import { connectPipelineWebSocket } from '../services/websocket';
import { mockLiveTerminalLogs } from '../services/mockData';

const WebSocketContext = createContext(null);

export const WebSocketProvider = ({ children }) => {
  const [status, setStatus] = useState('CONNECTING');
  const [pipelineState, setPipelineState] = useState({
    activeStep: 'synthesize',
    iteration: 1,
    maxIterations: 5,
    lastEvent: null,
  });
  const [liveLogs, setLiveLogs] = useState(mockLiveTerminalLogs);

  useEffect(() => {
    const client = connectPipelineWebSocket(
      (data) => {
        if (data.event === 'NODE_TRANSITION') {
          setPipelineState((prev) => ({
            ...prev,
            activeStep: data.payload?.node || prev.activeStep,
            iteration: data.payload?.iteration || prev.iteration,
            lastEvent: data,
          }));
        }
        if (data.payload?.log_line) {
          setLiveLogs((prev) => [...prev, data.payload.log_line]);
        }
      },
      (newStatus) => {
        setStatus(newStatus);
      }
    );

    return () => client.disconnect();
  }, []);

  const addLog = (logText) => {
    setLiveLogs((prev) => [...prev, logText]);
  };

  const clearLogs = () => {
    setLiveLogs([]);
  };

  return (
    <WebSocketContext.Provider
      value={{
        status,
        pipelineState,
        setPipelineState,
        liveLogs,
        addLog,
        clearLogs,
      }}
    >
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocket = () => {
  const ctx = useContext(WebSocketContext);
  if (!ctx) throw new Error('useWebSocket must be used within a WebSocketProvider');
  return ctx;
};

