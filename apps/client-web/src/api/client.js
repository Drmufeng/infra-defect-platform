import { request } from './request';

export const fetchClientProfile = () => request('/client/access/profile');

export const submitClientReport = (payload) =>
  request('/client/access/reports', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
