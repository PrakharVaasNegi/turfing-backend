import { Navigate } from "react-router-dom";
import { getToken } from "../api.js";

export default function RequireOwner({ children }) {
  if (!getToken()) return <Navigate to="/owner/login" replace />;
  return children;
}
