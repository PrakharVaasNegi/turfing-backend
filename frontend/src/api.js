const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const TOKEN_KEY = "turfing_owner_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

async function request(path, { method = "GET", body, auth = false } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (auth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Token ${token}`;
  }

  const res = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await res.text();
  const payload = text ? JSON.parse(text) : null;

  if (!res.ok) {
    const err = new Error("Request failed");
    err.status = res.status;
    err.errors = payload?.errors || [];
    err.firstMessage = err.errors[0]?.message || "Something went wrong.";
    throw err;
  }
  return payload?.result ?? payload;
}

// -- Public --
export async function listTurfs() {
  const r = await request("/api/turfs/");
  return r.turfs || [];
}
export async function getTurf(turfId) {
  const r = await request(`/api/turfs/${turfId}/`);
  return r.turf;
}
export async function listTurfSlots(turfId, { onlyAvailable = true } = {}) {
  const qs = onlyAvailable ? "?only_available=true" : "";
  const r = await request(`/api/turfs/${turfId}/slots/${qs}`);
  return r.slots || [];
}
export async function createBooking({ name, whatsappNumber, slotId }) {
  const r = await request("/api/bookings/", {
    method: "POST",
    body: { name, whatsapp_number: whatsappNumber, slot_id: slotId },
  });
  return r.booking;
}
export async function lookupBookings(phone) {
  const r = await request(`/api/bookings/?phone=${encodeURIComponent(phone)}`);
  return r.bookings || [];
}

// -- Owner auth --
export async function registerOwner(data) {
  const r = await request("/api/owner/register/", { method: "POST", body: data });
  setToken(r.token);
  return r.owner;
}
export async function loginOwner({ email, password }) {
  const r = await request("/api/owner/login/", {
    method: "POST",
    body: { email, password },
  });
  setToken(r.token);
  return r.owner;
}
export function logoutOwner() {
  setToken(null);
}

// -- Owner data --
export async function listOwnerTurfs() {
  const r = await request("/api/owner/turfs/", { auth: true });
  return r.turfs || [];
}
export async function createOwnerTurf(data) {
  const r = await request("/api/owner/turfs/", {
    method: "POST", auth: true, body: data,
  });
  return r.turf;
}
export async function listOwnerTurfSlots(turfId) {
  const r = await request(`/api/owner/turfs/${turfId}/slots/`, { auth: true });
  return r.slots || [];
}
export async function createOwnerSlot(turfId, data) {
  const r = await request(`/api/owner/turfs/${turfId}/slots/`, {
    method: "POST", auth: true, body: data,
  });
  return r.slot;
}
export async function bulkCreateOwnerSlots(turfId, slots) {
  const r = await request(`/api/owner/turfs/${turfId}/slots/bulk/`, {
    method: "POST", auth: true, body: { slots },
  });
  return r;
}
export async function listOwnerBookings() {
  const r = await request("/api/owner/bookings/", { auth: true });
  return r.bookings || [];
}
