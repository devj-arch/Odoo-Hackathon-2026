const TOKEN_KEY = "transitops_token";
const USER_KEY = "transitops_user";

export function getToken() {
  return (
    window.localStorage.getItem(TOKEN_KEY) ||
    window.sessionStorage.getItem(TOKEN_KEY)
  );
}

export function getStoredUser() {
  const raw =
    window.localStorage.getItem(USER_KEY) ||
    window.sessionStorage.getItem(USER_KEY);

  return raw ? JSON.parse(raw) : null;
}

export function setSession({ token, user, remember }) {
  const storage = remember ? window.localStorage : window.sessionStorage;
  storage.setItem(TOKEN_KEY, token);
  storage.setItem(USER_KEY, JSON.stringify(user));
}

export function clearSession() {
  window.localStorage.removeItem(TOKEN_KEY);
  window.localStorage.removeItem(USER_KEY);
  window.sessionStorage.removeItem(TOKEN_KEY);
  window.sessionStorage.removeItem(USER_KEY);
}