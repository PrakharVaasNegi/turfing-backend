import { useEffect } from "react";

export default function ConfirmModal({
  open,
  title = "Confirm booking",
  summary,
  phone,
  onCancel,
  onConfirm,
  submitting,
  error,
}) {
  useEffect(() => {
    if (!open) return;
    const onKey = (e) => { if (e.key === "Escape") onCancel?.(); };
    window.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [open, onCancel]);

  if (!open) return null;

  return (
    <div className="modal-backdrop" onClick={onCancel}>
      <div
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        onClick={(e) => e.stopPropagation()}
      >
        <h3 id="modal-title">{title}</h3>

        <dl className="modal-summary">
          {summary.map(({ label, value }) => (
            <div key={label} className="modal-row">
              <dt>{label}</dt>
              <dd>{value}</dd>
            </div>
          ))}
        </dl>

        <div className="modal-whatsapp">
          <span className="wa-chip" aria-hidden>WA</span>
          <div>
            <strong>WhatsApp confirmation</strong>
            <div className="muted">We'll send the booking details to <strong>{phone}</strong>.</div>
          </div>
        </div>

        {error && <p className="error">{error}</p>}

        <div className="modal-actions">
          <button
            type="button"
            className="btn-ghost"
            onClick={onCancel}
            disabled={submitting}
          >
            Cancel
          </button>
          <button
            type="button"
            className="btn-primary"
            onClick={onConfirm}
            disabled={submitting}
          >
            {submitting ? "Booking…" : "Confirm & send WhatsApp"}
          </button>
        </div>
      </div>
    </div>
  );
}
