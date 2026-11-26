import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { loginOwner } from "../api.js";

export default function OwnerLoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      await loginOwner({ email, password });
      navigate("/owner");
    } catch (err) {
      setError(err.firstMessage || "Login failed.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main>
      <section className="card narrow">
        <h2>Owner login</h2>
        <form className="form" onSubmit={handleSubmit}>
          <label>
            Email
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </label>
          <label>
            Password
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </label>
          <button type="submit" disabled={submitting}>
            {submitting ? "Logging in…" : "Log in"}
          </button>
          {error && <p className="error">{error}</p>}
        </form>
        <p className="muted">
          Don't have an account? <Link to="/owner/register">Register your turf</Link>.
        </p>
      </section>
    </main>
  );
}
