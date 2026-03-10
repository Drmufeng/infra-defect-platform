const TOKEN_KEY = 'rdp_admin_token';
const USER_KEY = 'rdp_admin_user';

export function getAccessToken() {
  return window.localStorage.getItem(TOKEN_KEY) || '';
}

export function getStoredUser() {
  const raw = window.localStorage.getItem(USER_KEY);
  if (!raw) {
    return null;
  }
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function setAuthSession({ accessToken, user }) {
  window.localStorage.setItem(TOKEN_KEY, accessToken);
  window.localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function clearAuthSession() {
  window.localStorage.removeItem(TOKEN_KEY);
  window.localStorage.removeItem(USER_KEY);
}

export function isLoggedIn() {
  return Boolean(getAccessToken());
}
