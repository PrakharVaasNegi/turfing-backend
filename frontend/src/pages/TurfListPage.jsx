import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { listTurfs } from "../api.js";
import Hero from "../components/Hero.jsx";

export default function TurfListPage() {
  const [turfs, setTurfs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        setTurfs(await listTurfs());
      } catch (e) {
        setError("Couldn't load turfs. Is the backend running?");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <main>
      <Hero />
      <section id="turfs" className="card">
        <h2>Pick a turf</h2>
        {loading && <p>Loading turfs…</p>}
        {error && <p className="error">{error}</p>}
        {!loading && !error && turfs.length === 0 && (
          <p className="muted">
            No turfs listed yet. If you're a turf owner,{" "}
            <Link to="/owner/register">sign up</Link> to add yours.
          </p>
        )}
        <ul className="turf-list">
          {turfs.map((t, i) => (
            <li
              key={t.id}
              className="turf-card stagger-in"
              style={{ animationDelay: `${i * 70}ms` }}
            >
              <Link
                to={`/turfs/${t.id}`}
                onMouseMove={(e) => {
                  const r = e.currentTarget.getBoundingClientRect();
                  e.currentTarget.style.setProperty("--mx", `${e.clientX - r.left}px`);
                  e.currentTarget.style.setProperty("--my", `${e.clientY - r.top}px`);
                }}
              >
                <div className="turf-card-glow" aria-hidden />
                <h3>{t.name}</h3>
                <p className="muted">{t.location}</p>
                {t.description && <p>{t.description}</p>}
                <span className="turf-card-arrow">Book now →</span>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
