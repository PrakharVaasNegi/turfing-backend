export default function BackgroundFX() {
  return (
    <div className="bg-fx" aria-hidden>
      <div className="bg-field" />
      <div className="bg-blob bg-blob-1" />
      <div className="bg-blob bg-blob-2" />
      <div className="bg-blob bg-blob-3" />
      <div className="bg-particles">
        {Array.from({ length: 14 }).map((_, i) => (
          <span
            key={i}
            className="bg-particle"
            style={{
              left: `${(i * 73) % 100}%`,
              animationDelay: `${(i * 1.7) % 10}s`,
              animationDuration: `${12 + (i % 6) * 2}s`,
            }}
          >
            <svg viewBox="-16 -16 32 32" width="18" height="18">
              <circle r="14" fill="#ffffff" stroke="#0a0f1a" strokeWidth="1.2" />
              <polygon
                points="0,-5 4.76,-1.55 2.94,4.05 -2.94,4.05 -4.76,-1.55"
                fill="#0a0f1a"
              />
              <line x1="0" y1="-5" x2="0" y2="-14" stroke="#0a0f1a" />
              <line x1="4.76" y1="-1.55" x2="13.3" y2="-4.3" stroke="#0a0f1a" />
              <line x1="2.94" y1="4.05" x2="8.2" y2="11.3" stroke="#0a0f1a" />
              <line x1="-2.94" y1="4.05" x2="-8.2" y2="11.3" stroke="#0a0f1a" />
              <line x1="-4.76" y1="-1.55" x2="-13.3" y2="-4.3" stroke="#0a0f1a" />
            </svg>
          </span>
        ))}
      </div>
    </div>
  );
}
