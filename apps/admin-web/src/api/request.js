const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

import { clearAuthSession, getAccessToken } from '@/shared/utils/auth';

// 统一封装前端请求入口，后续若要接鉴权、错误上报或请求拦截，可在这里集中扩展。
export async function request(path, options = {}) {
  const accessToken = getAccessToken();
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(accessToken && !options.skipAuth ? { Authorization: `Bearer ${accessToken}` } : {}),
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const message = await response.text();
    let normalizedMessage = message;
    try {
      const parsed = JSON.parse(message);
      normalizedMessage = parsed.detail || parsed.message || message;
    } catch {
      normalizedMessage = message;
    }
    if (response.status === 401 && !options.skipAuth) {
      clearAuthSession();
      if (window.location.hash !== '#/login') {
        window.location.hash = '#/login';
      }
    }
    throw new Error(normalizedMessage || `Request failed: ${response.status}`);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}
