import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerOwner } from "../api.js";

export default function OwnerRegisterPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    email: "", password: "", business_name: "", whatsapp_number: "",
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  function setField(k, v) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      await registerOwner(form);
      navigate("/owner");
    } catch (err) {
      setError(err.firstMessage || "Registration failed.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main>
      <section className="card narrow">
        <h2>Register as a turf owner</h2>
        <form className="form" onSubmit={handleSubmit}>
          <label>
            Business name
            <input type="text" value={form.business_name}
              onChange={(e) => setField("business_name", e.target.value)} required />
          </label>
          <label>
            Email
            <input type="email" value={form.email}
              onChange={(e) => setField("email", e.target.value)} required />
          </label>
          <label>
            Password
            <input type="password" value={form.password}
              onChange={(e) => setField("password", e.target.value)} required minLength={8} />
          </label>
          <label>
            WhatsApp number (for booking alerts)
            <input type="tel" value={form.whatsapp_number}
              onChange={(e) => setField("whatsapp_number", e.target.value)}
              required pattern="^\+[1-9]\d{7,14}$" placeholder="+919812345678" />
          </label>
          <button type="submit" disabled={submitting}>
            {submitting ? "Creating account…" : "Create account"}
          </button>
          {error && <p className="error">{error}</p>}
        </form>
        <p className="muted">
          Already have an account? <Link to="/owner/login">Log in</Link>.
        </p>
      </section>
    </main>
  );
}
