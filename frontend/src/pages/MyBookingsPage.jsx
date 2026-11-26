import { useState } from "react";
import { lookupBookings } from "../api.js";

export default function MyBookingsPage() {
  const [phone, setPhone] = useState("");
  const [bookings, setBookings] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setBookings(null);
    try {
      setBookings(await lookupBookings(phone.trim()));
    } catch (err) {
      setError(err.firstMessage || "Couldn't look up bookings.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <section className="card">
        <h2>Look up your bookings</h2>
        <form className="form" onSubmit={handleSubmit}>
          <label>
            WhatsApp number
            <input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)}
              placeholder="+919812345678" required pattern="^\+[1-9]\d{7,14}$" />
          </label>
          <button type="submit" disabled={loading}>
            {loading ? "Looking up…" : "Find my bookings"}
          </button>
        </form>

        {error && <p className="error">{error}</p>}

        {bookings && bookings.length === 0 && (
          <p className="muted">No bookings found for that number.</p>
        )}

        {bookings && bookings.length > 0 && (
          <ul className="booking-list">
            {bookings.map((b) => (
              <li key={b.id} className="booking">
                <div><strong>#{b.id}</strong> — {b.name}</div>
                <div>
                  {b.slot.turf_name} · {new Date(b.slot.start_time).toLocaleString()}
                </div>
                <div className="muted">
                  {b.status} · WhatsApp {b.notification_status}
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
