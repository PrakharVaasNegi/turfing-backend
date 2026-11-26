import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { createBooking, getTurf, listTurfSlots } from "../api.js";
import ConfirmModal from "../components/ConfirmModal.jsx";

function fmt(iso) {
  return new Date(iso).toLocaleString(undefined, {
    weekday: "short", day: "2-digit", month: "short",
    hour: "2-digit", minute: "2-digit",
  });
}

export default function TurfDetailPage() {
  const { turfId } = useParams();
  const [turf, setTurf] = useState(null);
  const [slots, setSlots] = useState([]);
  const [selected, setSelected] = useState(null);
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(null);
  const [showConfirm, setShowConfirm] = useState(false);
  const [confirmError, setConfirmError] = useState("");

  async function reload() {
    setLoading(true);
    setError("");
    try {
      const [t, s] = await Promise.all([getTurf(turfId), listTurfSlots(turfId)]);
      setTurf(t);
      setSlots(s);
    } catch (e) {
      setError("Couldn't load this turf.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { reload(); /* eslint-disable-next-line */ }, [turfId]);

  function openConfirm(e) {
    e.preventDefault();
    setError("");
    setConfirmError("");
    if (!selected) {
      setError("Pick a slot first.");
      return;
    }
    setShowConfirm(true);
  }

  async function handleConfirm() {
    setSubmitting(true);
    setConfirmError("");
    try {
      const booking = await createBooking({
        name: name.trim(),
        whatsappNumber: phone.trim(),
        slotId: selected.id,
      });
      setSuccess(booking);
      setShowConfirm(false);
      setSelected(null);
      setName("");
      setPhone("");
      reload();
    } catch (err) {
      setConfirmError(err.firstMessage || "Booking failed.");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) return <main><section className="card">Loading…</section></main>;
  if (!turf) return <main><section className="card">Turf not found. <Link to="/">Back</Link></section></main>;

  return (
    <main className="grid">
      <section className="card">
        <Link to="/" className="back-link">← Back to turfs</Link>
        <h2>{turf.name}</h2>
        <p className="muted">{turf.location}</p>
        {turf.description && <p>{turf.description}</p>}

        <h3>Available slots</h3>
        {slots.length === 0 ? (
          <p className="muted">No open slots right now. Check back soon.</p>
        ) : (
          <ul className="slot-list">
            {slots.map((slot) => {
              const isSelected = selected?.id === slot.id;
              return (
                <li key={slot.id}>
                  <button
                    className={isSelected ? "slot selected" : "slot"}
                    onClick={() => setSelected(slot)}
                    disabled={slot.is_booked}
                  >
                    <span className="slot-time">{fmt(slot.start_time)}</span>
                    <span className="slot-meta">
                      {slot.duration_minutes} min · ₹{slot.price}
                    </span>
                  </button>
                </li>
              );
            })}
          </ul>
        )}
      </section>

      <section className="card">
        <h2>Your details</h2>
        <form className="form" onSubmit={openConfirm}>
          {selected ? (
            <p className="selected-slot">
              Selected: <strong>{fmt(selected.start_time)}</strong>
              {" · "}₹{selected.price}
            </p>
          ) : (
            <p className="muted">Select a slot to continue.</p>
          )}
          <label>
            Your name
            <input type="text" value={name} onChange={(e) => setName(e.target.value)}
              placeholder="Alex Doe" required minLength={2} />
          </label>
          <label>
            WhatsApp number
            <input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)}
              placeholder="+919812345678" required pattern="^\+[1-9]\d{7,14}$"
              title="Use E.164 format, e.g. +919812345678" />
          </label>
          <button type="submit" disabled={!selected}>
            Review & confirm
          </button>
          {error && <p className="error">{error}</p>}
          {success && (
            <div className="success">
              <p>✓ Booking #{success.id} confirmed for {success.name}.</p>
              <p>
                {success.notification_status === "sent"
                  ? `WhatsApp confirmation sent to ${success.whatsapp_number}.`
                  : success.notification_status === "dry_run"
                  ? "Twilio not configured — the message was logged on the server."
                  : "WhatsApp confirmation pending."}
              </p>
            </div>
          )}
        </form>
      </section>

      <ConfirmModal
        open={showConfirm}
        phone={phone}
        onCancel={() => !submitting && setShowConfirm(false)}
        onConfirm={handleConfirm}
        submitting={submitting}
        error={confirmError}
        summary={selected ? [
          { label: "Turf", value: turf.name },
          { label: "Where", value: turf.location },
          { label: "When", value: fmt(selected.start_time) },
          { label: "Duration", value: `${selected.duration_minutes} min` },
          { label: "Price", value: `₹${selected.price}` },
          { label: "Name", value: name },
          { label: "WhatsApp", value: phone },
        ] : []}
      />
    </main>
  );
}
