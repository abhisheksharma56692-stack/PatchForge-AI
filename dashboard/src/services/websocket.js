/**
 * WebSocket client with automatic reconnection for live pipeline state streaming.
 */
export function connectPipelineWebSocket(onMessage, onStatusChange) {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const host = window.location.host;
  const wsUrl = `${protocol}//${host}/ws/pipeline`;

  let ws = null;
  let isClosed = false;

  function connect() {
    try {
      ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        if (onStatusChange) onStatusChange('CONNECTED');
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          onMessage(data);
        } catch {
          onMessage(event.data);
        }
      };

      ws.onclose = () => {
        if (!isClosed) {
          if (onStatusChange) onStatusChange('RECONNECTING');
          setTimeout(connect, 3000);
        }
      };

      ws.onerror = () => {
        ws.close();
      };
    } catch {
      setTimeout(connect, 3000);
    }
  }

  connect();

  return {
    disconnect: () => {
      isClosed = true;
      if (ws) ws.close();
    },
    send: (msg) => {
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(typeof msg === 'string' ? msg : JSON.stringify(msg));
      }
    },
  };
}

