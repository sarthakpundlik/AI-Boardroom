import { useEffect, useRef, useState, useCallback } from "react";
import { WS_BASE, tokenStore } from "./api";

// Mirrors backend/app/websocket/events.py EventType enum exactly.
export const EVENT_TYPES = {
  AGENT_STARTED: "agent_started",
  AGENT_FINISHED: "agent_finished",
  ROUND_ADVANCED: "round_advanced",
  CEO_STARTED: "ceo_started",
  SESSION_COMPLETED: "session_completed",
  ERROR: "error",
};

/**
 * Connects to ws://.../ws/{sessionId}?token=... and keeps a running event
 * log plus derived per-agent status. Auto-reconnects with backoff if the
 * connection drops (useful since long boardroom runs can outlive a flaky
 * network). The backend requires the access token as a query param since
 * browsers can't set custom headers on the WebSocket handshake — see
 * backend/app/websocket/router.py.
 */
export function useBoardroomSocket(sessionId, { enabled = true } = {}) {
  const [connected, setConnected] = useState(false);
  const [events, setEvents] = useState([]);
  const [agentStatus, setAgentStatus] = useState({}); // { agentKey: 'idle'|'thinking'|'done' }
  const [round, setRound] = useState(1);
  const [error, setError] = useState(null);
  const [reportId, setReportId] = useState(null);
  const wsRef = useRef(null);
  const attemptRef = useRef(0);
  const closedByUserRef = useRef(false);

  const applyEvent = useCallback((evt) => {
    setEvents((prev) => [...prev, { ...evt, ts: Date.now() }]);

    switch (evt.type) {
      case EVENT_TYPES.AGENT_STARTED:
        setAgentStatus((prev) => ({ ...prev, [evt.payload.agent]: "thinking" }));
        break;
      case EVENT_TYPES.AGENT_FINISHED:
        setAgentStatus((prev) => ({ ...prev, [evt.payload.agent]: "done" }));
        break;
      case EVENT_TYPES.CEO_STARTED:
        setAgentStatus((prev) => ({ ...prev, CEO: "thinking" }));
        break;
      case EVENT_TYPES.ROUND_ADVANCED:
        setRound(evt.payload.round ?? evt.payload.current_round ?? 1);
        setAgentStatus({});
        break;
      case EVENT_TYPES.SESSION_COMPLETED:
        setAgentStatus((prev) => ({ ...prev, CEO: "done" }));
        if (evt.payload?.report_id) setReportId(evt.payload.report_id);
        break;
      case EVENT_TYPES.ERROR:
        setError(evt.payload?.message || "The boardroom session hit an error.");
        break;
      default:
        break;
    }
  }, []);

  useEffect(() => {
    if (!enabled || !sessionId) return;
    closedByUserRef.current = false;

    let socket;
    let reconnectTimer;

    const connect = () => {
      const token = tokenStore.access;
      socket = new WebSocket(`${WS_BASE}/${sessionId}?token=${encodeURIComponent(token || "")}`);
      wsRef.current = socket;

      socket.onopen = () => {
        setConnected(true);
        attemptRef.current = 0;
      };

      socket.onmessage = (msg) => {
        try {
          const evt = JSON.parse(msg.data);
          applyEvent(evt);
        } catch {
          // Non-JSON frame — ignore rather than crash the visualization.
        }
      };

      socket.onclose = () => {
        setConnected(false);
        if (closedByUserRef.current) return;
        const delay = Math.min(1000 * 2 ** attemptRef.current, 10000);
        attemptRef.current += 1;
        reconnectTimer = setTimeout(connect, delay);
      };

      socket.onerror = () => {
        socket.close();
      };
    };

    connect();

    return () => {
      closedByUserRef.current = true;
      clearTimeout(reconnectTimer);
      socket?.close();
    };
  }, [sessionId, enabled, applyEvent]);

  const reset = useCallback(() => {
    setEvents([]);
    setAgentStatus({});
    setRound(1);
    setError(null);
    setReportId(null);
  }, []);

  return { connected, events, agentStatus, round, error, reportId, reset };
}
