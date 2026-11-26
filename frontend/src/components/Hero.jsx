import { Link } from "react-router-dom";

export default function Hero() {
  return (
    <section className="hero">
      <div className="hero-inner">
        <p className="hero-kicker">PLAY · BOOK · REPEAT</p>
        <h1 className="hero-title">
          Your next <span className="shimmer">match</span> starts here.
        </h1>
        <p className="hero-sub">
          Browse turfs around you, lock a slot in seconds, and get your
          confirmation straight on WhatsApp.
        </p>
        <div className="hero-cta">
          <a href="#turfs" className="btn-primary">Browse turfs</a>
          <Link to="/owner/register" className="btn-ghost">
            List your turf →
          </Link>
        </div>
      </div>
      <div className="hero-pitch" aria-hidden>
        <div className="pitch-line pitch-line-h" />
        <div className="pitch-line pitch-line-v" />
        <div className="pitch-circle" />
        <div className="pitch-dot" />
      </div>
    </section>
  );
}
