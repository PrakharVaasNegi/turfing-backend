import { useEffect, useRef } from "react";

export default function FootballCursor() {
  const cursorRef = useRef(null);
  const trailRefs = useRef([]);
  const pos = useRef({ x: 0, y: 0, tx: 0, ty: 0, rot: 0 });
  const trail = useRef([
    { x: 0, y: 0 }, { x: 0, y: 0 }, { x: 0, y: 0 },
  ]);
  const clicking = useRef(false);

  useEffect(() => {
    const handleMove = (e) => {
      pos.current.tx = e.clientX;
      pos.current.ty = e.clientY;
    };
    const handleDown = () => (clicking.current = true);
    const handleUp = () => (clicking.current = false);

    window.addEventListener("mousemove", handleMove);
    window.addEventListener("mousedown", handleDown);
    window.addEventListener("mouseup", handleUp);

    let raf;
    const loop = () => {
      const p = pos.current;
      const dx = p.tx - p.x;
      const dy = p.ty - p.y;
      p.x += dx * 0.22;
      p.y += dy * 0.22;
      const speed = Math.hypot(dx, dy);
      p.rot += speed * 0.6;

      // Trail lags more and more
      const dampings = [0.14, 0.09, 0.055];
      trail.current.forEach((t, i) => {
        t.x += (p.x - t.x) * dampings[i];
        t.y += (p.y - t.y) * dampings[i];
        const el = trailRefs.current[i];
        if (el) {
          el.style.transform = `translate3d(${t.x - 10}px, ${t.y - 10}px, 0)`;
          el.style.opacity = String(Math.min(speed / 40, 0.5) * (1 - i * 0.25));
        }
      });

      if (cursorRef.current) {
        const scale = clicking.current ? 0.75 : 1;
        cursorRef.current.style.transform =
          `translate3d(${p.x - 14}px, ${p.y - 14}px, 0) rotate(${p.rot}deg) scale(${scale})`;
      }
      raf = requestAnimationFrame(loop);
    };
    raf = requestAnimationFrame(loop);

    return () => {
      window.removeEventListener("mousemove", handleMove);
      window.removeEventListener("mousedown", handleDown);
      window.removeEventListener("mouseup", handleUp);
      cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <>
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          ref={(el) => (trailRefs.current[i] = el)}
          className="football-trail"
          aria-hidden
        />
      ))}
      <div ref={cursorRef} className="football-cursor" aria-hidden>
        <svg viewBox="-16 -16 32 32" width="28" height="28">
          <circle r="15" fill="#ffffff" stroke="#0a0f1a" strokeWidth="1.2" />
          {/* central pentagon */}
          <polygon
            points="0,-5 4.76,-1.55 2.94,4.05 -2.94,4.05 -4.76,-1.55"
            fill="#0a0f1a"
          />
          {/* lines radiating to the edge */}
          <line x1="0" y1="-5" x2="0" y2="-15" stroke="#0a0f1a" strokeWidth="1.2" />
          <line x1="4.76" y1="-1.55" x2="14.27" y2="-4.64" stroke="#0a0f1a" strokeWidth="1.2" />
          <line x1="2.94" y1="4.05" x2="8.82" y2="12.14" stroke="#0a0f1a" strokeWidth="1.2" />
          <line x1="-2.94" y1="4.05" x2="-8.82" y2="12.14" stroke="#0a0f1a" strokeWidth="1.2" />
          <line x1="-4.76" y1="-1.55" x2="-14.27" y2="-4.64" stroke="#0a0f1a" strokeWidth="1.2" />
        </svg>
      </div>
    </>
  );
}
