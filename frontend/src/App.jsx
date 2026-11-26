import { Link, NavLink, Route, Routes, useLocation, useNavigate } from "react-router-dom";
import { getToken, logoutOwner } from "./api.js";
import TurfListPage from "./pages/TurfListPage.jsx";
import TurfDetailPage from "./pages/TurfDetailPage.jsx";
import MyBookingsPage from "./pages/MyBookingsPage.jsx";
import OwnerLoginPage from "./pages/OwnerLoginPage.jsx";
import OwnerRegisterPage from "./pages/OwnerRegisterPage.jsx";
import OwnerDashboardPage from "./pages/OwnerDashboardPage.jsx";
import OwnerTurfCreatePage from "./pages/OwnerTurfCreatePage.jsx";
import OwnerTurfManagePage from "./pages/OwnerTurfManagePage.jsx";
import RequireOwner from "./components/RequireOwner.jsx";
import FootballCursor from "./components/FootballCursor.jsx";
import BackgroundFX from "./components/BackgroundFX.jsx";

export default function App() {
  const navigate = useNavigate();
  const location = useLocation();
  const loggedIn = Boolean(getToken());

  function handleLogout() {
    logoutOwner();
    navigate("/owner/login");
  }

  return (
    <div className="app">
      <BackgroundFX />
      <FootballCursor />
      <header className="header">
        <div className="brand">
          <Link to="/">Turfing</Link>
          <span className="tagline">Book turf slots across the city.</span>
        </div>
        <nav className="main-nav">
          <NavLink to="/" end>Browse turfs</NavLink>
          <NavLink to="/my-bookings">My bookings</NavLink>
          {loggedIn ? (
            <>
              <NavLink to="/owner">Owner dashboard</NavLink>
              <button className="link-btn" onClick={handleLogout}>Log out</button>
            </>
          ) : (
            <NavLink to="/owner/login">Owner login</NavLink>
          )}
        </nav>
      </header>

      <div key={location.pathname} className="route-fade">
      <Routes>
        <Route path="/" element={<TurfListPage />} />
        <Route path="/turfs/:turfId" element={<TurfDetailPage />} />
        <Route path="/my-bookings" element={<MyBookingsPage />} />

        <Route path="/owner/login" element={<OwnerLoginPage />} />
        <Route path="/owner/register" element={<OwnerRegisterPage />} />

        <Route path="/owner" element={<RequireOwner><OwnerDashboardPage /></RequireOwner>} />
        <Route path="/owner/turfs/new" element={<RequireOwner><OwnerTurfCreatePage /></RequireOwner>} />
        <Route path="/owner/turfs/:turfId" element={<RequireOwner><OwnerTurfManagePage /></RequireOwner>} />
      </Routes>
      </div>

      <footer className="footer">
        <small>Players get a WhatsApp confirmation; turf owners get notified on every booking.</small>
      </footer>
    </div>
  );
}
