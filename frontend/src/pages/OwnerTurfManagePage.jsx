import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { bulkCreateOwnerSlots, listOwnerTurfSlots } from "../api.js";

function pad(n) { return String(n).padStart(2, "0"); }
function todayISO() {
  const d = new Date();
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}
function fmtHour(h) {
  const period = h >= 12 ? "PM" : "AM";
  const hr = h % 12 === 0 ? 12 : h % 12;
  return `${hr}:00 ${period}`;
}

function buildSlotPreview({ date, startHour, endHour, durationMinutes, price }) {
  if (endHour < startHour) return [];
  const out = [];
  for (let h = startHour; h <= endHour; h++) {
    const start = new Date(`${date}T${pad(h)}:00:00`);
    out.push({
      key: `${date}-${h}`,
      start_time: start.toISOString(),
      hour: h,
      duration_minutes: durationMinutes,
      price,
    });
  }
  return out;
}

export default function OwnerTurfManagePage() {
  const { turfId } = useParams();
  const [slots, setSlots] = useState([]);
  const [loading, setLoading] = useState(true);

  // Bulk form state
  const [date, setDate] = useState(todayISO());
  const [startHour, setStartHour] = useState(6);
  const [endHour, setEndHour] = useState(23);
  const [durationMinutes, setDurationMinutes] = useState(60);
  const [defaultPrice, setDefaultPrice] = useState("500");
  const [preview, setPreview] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  async function reload() {
    setLoading(true);
    try {
      setSlots(await listOwnerTurfSlots(turfId));
    } finally {
      setLoading(false);
    }
  }
  useEffect(() => { reload(); /* eslint-disable-next-line */ }, [turfId]);

  const generatedCount = useMemo(() => preview.length, [preview]);

  function handleGenerate(e) {
    e?.preventDefault();
    setError("");
    setSuccessMsg("");
    const list = buildSlotPreview({
      date,
      startHour: Number(startHour),
      endHour: Number(endHour),
      durationMinutes: Number(durationMinutes),
      price: defaultPrice,
    });
    if (!list.length) {
      setError("End hour must be the same as or after the start hour.");
      setPreview([]);
      return;
    }
    setPreview(list);
  }

  function updateSlotPrice(key, value) {
    setPreview((p) => p.map((s) => (s.key === key ? { ...s, price: value } : s)));
  }

  function applyPriceToAll() {
    setPreview((p) => p.map((s) => ({ ...s, price: defaultPrice })));
  }

  function removeSlot(key) {
    setPreview((p) => p.filter((s) => s.key !== key));
  }

  async function handleCreateAll() {
    if (!preview.length) return;
    setSubmitting(true);
    setError("");
    setSuccessMsg("");
    try {
      const payload = preview.map((s) => ({
        start_time: s.start_time,
        duration_minutes: s.duration_minutes,
        price: s.price,
      }));
      const r = await bulkCreateOwnerSlots(turfId, payload);
      setSuccessMsg(
        `Created ${r.created_count} slot${r.created_count === 1 ? "" : "s"}` +
        (r.skipped_count ? ` · skipped ${r.skipped_count} (already exist)` : "")
      );
      setPreview([]);
      reload();
    } catch (err) {
      setError(err.firstMessage || "Couldn't create slots.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="grid">
      <section className="card">
        <Link to="/owner" className="back-link">← Back to dashboard</Link>
        <h2>Generate slots</h2>
        <p className="muted" style={{ marginTop: 0 }}>
          Create a full day's slots in one go. You can tweak individual prices
          before locking them in.
        </p>

        <form className="form" onSubmit={handleGenerate}>
          <label>
            Date
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              required
            />
          </label>
          <div className="form-row">
            <label>
              From
              <select value={startHour} onChange={(e) => setStartHour(e.target.value)}>
                {Array.from({ length: 24 }).map((_, h) => (
                  <option key={h} value={h}>{fmtHour(h)}</option>
                ))}
              </select>
            </label>
            <label>
              To (last slot)
              <select value={endHour} onChange={(e) => setEndHour(e.target.value)}>
                {Array.from({ length: 24 }).map((_, h) => (
                  <option key={h} value={h}>{fmtHour(h)}</option>
                ))}
              </select>
            </label>
          </div>
          <div className="form-row">
            <label>
              Duration (min)
              <input
                type="number" min="15" max="240"
                value={durationMinutes}
                onChange={(e) => setDurationMinutes(e.target.value)}
              />
            </label>
            <label>
              Default price (₹)
              <input
                type="number" step="0.01" min="0"
                value={defaultPrice}
                onChange={(e) => setDefaultPrice(e.target.value)}
              />
            </label>
          </div>
          <button type="submit">Generate preview</button>
          {error && <p className="error">{error}</p>}
          {successMsg && <p className="success-inline">✓ {successMsg}</p>}
        </form>

        {preview.length > 0 && (
          <div className="preview">
            <div className="preview-head">
              <strong>{generatedCount} slot{generatedCount === 1 ? "" : "s"} ready</strong>
              <button
                type="button"
                className="link-btn"
                onClick={applyPriceToAll}
                title="Reset every slot to the default price"
              >
                Apply ₹{defaultPrice} to all
              </button>
            </div>
            <ul className="preview-list">
              {preview.map((s) => (
                <li key={s.key} className="preview-row">
                  <span className="preview-time">{fmtHour(s.hour)}</span>
                  <div className="preview-price">
                    <span>₹</span>
                    <input
                      type="number"
                      step="0.01"
                      min="0"
                      value={s.price}
                      onChange={(e) => updateSlotPrice(s.key, e.target.value)}
                    />
                  </div>
                  <button
                    type="button"
                    className="icon-btn"
                    onClick={() => removeSlot(s.key)}
                    aria-label="Remove slot"
                  >
                    ✕
                  </button>
                </li>
              ))}
            </ul>
            <button
              type="button"
              className="create-all"
              onClick={handleCreateAll}
              disabled={submitting}
            >
              {submitting ? "Creating…" : `Create ${generatedCount} slot${generatedCount === 1 ? "" : "s"}`}
            </button>
          </div>
        )}
      </section>

      <section className="card">
        <h2>Existing slots</h2>
        {loading && <p>Loading…</p>}
        {!loading && slots.length === 0 && (
          <p className="muted">No slots yet. Generate some on the left.</p>
        )}
        <ul className="booking-list">
          {slots.map((s) => (
            <li key={s.id} className="booking">
              <div>
                <strong>{new Date(s.start_time).toLocaleString()}</strong>
                {" · "}{s.duration_minutes} min · ₹{s.price}
              </div>
              <div className="muted">
                {s.is_booked ? "Booked" : "Open"} · {s.is_active ? "Active" : "Inactive"}
              </div>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
