import { useEffect, useState } from "react";

/**
 * Whole seconds since `start()`, counted once a second while `running` (step 7.12: "Bild wird
 * erzeugt … 12 s").
 */
export function useElapsed(running: boolean) {
  const [startedAt, setStartedAt] = useState(0);
  const [now, setNow] = useState(0);

  useEffect(() => {
    if (!running) {
      return;
    }
    const timer = window.setInterval(() => {
      setNow(Date.now());
    }, 1000);
    return () => {
      window.clearInterval(timer);
    };
  }, [running]);

  function start() {
    const at = Date.now();
    setStartedAt(at);
    setNow(at);
  }

  return { seconds: Math.max(0, Math.round((now - startedAt) / 1000)), start };
}
