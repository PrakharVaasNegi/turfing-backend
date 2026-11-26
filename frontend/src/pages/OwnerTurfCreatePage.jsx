import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { createOwnerTurf } from "../api.js";

export default function OwnerTurfCreatePage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: "", location: "", description: "", image_url: "",
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  function setField(k, v) { setForm((f) => ({ ...f, [k]: v })); }

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      const turf = await createOwnerTurf(form);
      navigate(`/owner/turfs/${turf.id}`);
    } catch (err) {
      setError(err.firstMessage || "Couldn't create turf.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main>
      <section className="card narrow">
        <Link to="/owner" className="back-link">← Back to dashboard</Link>
        <h2>Add a turf</h2>
        <form className="form" onSubmit={handleSubmit}>
          <label>
            Name
            <input value={form.name} onChange={(e) => setField("name", e.target.value)} required />
          </label>
          <label>
            Location
            <input value={form.location} onChange={(e) => setField("location", e.target.value)} required />
          </label>
          <label>
            Description
            <textarea rows="3" value={form.description}
              onChange={(e) => setField("description", e.target.value)} />
          </label>
          <label>
            Image URL (optional)
            <input type="url" value={form.image_url}
              onChange={(e) => setField("image_url", e.target.value)} />
          </label>
          <button type="submit" disabled={submitting}>
            {submitting ? "Saving…" : "Create turf"}
          </button>
          {error && <p className="error">{error}</p>}
        </form>
      </section>
    </main>
  );
}
