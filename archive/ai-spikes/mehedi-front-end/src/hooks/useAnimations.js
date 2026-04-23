import { useState, useEffect } from 'react';

export function useCountUp(target, duration = 1000) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    if (target === 0) {
      setCount(0);
      return;
    }

    const steps = 60;
    const stepDuration = duration / steps;
    const increment = target / steps;
    let current = 0;
    let step = 0;

    const interval = setInterval(() => {
      step++;
      current += increment;
      if (step >= steps) {
        setCount(Math.round(target));
        clearInterval(interval);
      } else {
        setCount(Math.round(current));
      }
    }, stepDuration);

    return () => clearInterval(interval);
  }, [target, duration]);

  return count;
}

export function useSystemStatus() {
  const [status, setStatus] = useState('online');

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await fetch('http://localhost:8000/socratic', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ topic: 'test', previousAnswer: '' })
        });
        setStatus(response.ok ? 'online' : 'degraded');
      } catch {
        setStatus('degraded');
      }
    };

    checkStatus();
    const interval = setInterval(checkStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  return status;
}
