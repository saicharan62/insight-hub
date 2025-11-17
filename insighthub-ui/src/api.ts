export const API = (path: string) =>
  `${(window as any).__INSIGHTHUB_API_BASE__ || "http://127.0.0.1:8000"}${path}`;

export async function authLogin(email: string, password: string) {
  const r = await fetch(API("/auth/login"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!r.ok) throw new Error("Login failed");
  return r.json();
}

export async function authRegister(email: string, password: string) {
  const r = await fetch(API("/auth/register"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!r.ok) throw new Error("Register failed");
  return r.json();
}
