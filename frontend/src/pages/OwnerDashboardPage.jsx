import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { listOwnerBookings, listOwnerTurfs } from "../api.js";

export default function OwnerDashboardPage() {
  const [turfs, setTurfs] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const [t, b] = await Promise.all([listOwnerTurfs(), listOwnerBookings()]);
        setTurfs(t);
        setBookings(b);
      } catch (e) {
        setError(e.firstMessage || "Couldn't load dashboard.");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return <main><section className="card">Loading…</section></main>;

  return (
    <main className="grid">
      <section className="card">
        <div className="section-head">
          <h2>Your turfs</h2>
          <Link to="/owner/turfs/new" className="action-btn">+ Add turf</Link>
        </div>
        {error && <p className="error">{error}</p>}
        {turfs.length === 0 && <p className="muted">No turfs yet. Add your first one.</p>}
        <ul className="turf-list">
          {turfs.map((t) => (
            <li key={t.id} className="turf-card">
              <Link to={`/owner/turfs/${t.id}`}>
                <h3>{t.name}</h3>
                <p className="muted">{t.location}</p>
                <p className="muted">{t.is_active ? "Active" : "Inactive"}</p>
              </Link>
            </li>
          ))}
        </ul>
      </section>

      <section className="card">
        <h2>Recent bookings</h2>
        {bookings.length === 0 && <p className="muted">No bookings yet.</p>}
        <ul className="booking-list">
          {bookings.slice(0, 10).map((b) => (
            <li key={b.id} className="booking">
              <div><strong>#{b.id}</strong> — {b.name} ({b.whatsapp_number})</div>
              <div>{b.slot.turf_name} · {new Date(b.slot.start_time).toLocaleString()}</div>
              <div className="muted">
                {b.status} · WhatsApp {b.notification_status}
              </div>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
