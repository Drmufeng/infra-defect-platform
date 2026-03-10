import { request } from '@/api/request';

export const login = (payload) =>
  request('/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload),
    skipAuth: true,
  });

export const fetchCurrentUser = () => request('/auth/me');

export const fetchOverview = () => request('/overview');
export const fetchRuntimeStatus = () => request('/overview/runtime');
export const fetchDatasets = () => request('/admin/datasets');
export const fetchTrainingJobs = () => request('/admin/training/jobs');
export const fetchTrainingMetrics = () => request('/admin/training/metrics');
export const fetchModels = () => request('/admin/models');
export const fetchTestingTasks = () => request('/admin/testing/tasks');
export const fetchArtifacts = () => request('/admin/artifacts');
export const fetchAuditLogs = () => request('/admin/audit-logs');
export const fetchSettings = () => request('/settings');

export const fetchClientProfile = () => request('/client/access/profile');

export const submitClientReport = (payload) =>
  request('/client/access/reports', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
