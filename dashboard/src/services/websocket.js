// WebSocket client for real-time pipeline telemetry streaming

export const connectPipelineWebSocket = (onMessage, onStatusChange) => {
  let ws = null;
  let reconnectTimer = null;
  let isManuallyClosed = false;

  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/ws/pipeline`;

  const connect = () => {
    try {
      ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        onStatusChange?.('CONNECTED');
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          onMessage?.(data);
        } catch {
          onMessage?.({ event: 'RAW_TEXT', data: event.data });
        }
      };

      ws.onerror = () => {
        onStatusChange?.('OFFLINE');
      };

      ws.onclose = () => {
        if (!isManuallyClosed) {
          onStatusChange?.('RECONNECTING');
          reconnectTimer = setTimeout(connect, 4000);
        } else {
          onStatusChange?.('DISCONNECTED');
        }
      };
    } catch {
      onStatusChange?.('OFFLINE');
    }
  };

  connect();

  return {
    send: (msg) => {
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(typeof msg === 'string' ? msg : JSON.stringify(msg));
      }
    },
    disconnect: () => {
      isManuallyClosed = true;
      clearTimeout(reconnectTimer);
      if (ws) ws.close();
    },
  };
};
