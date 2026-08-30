import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

// Request interceptor - add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('recoverai_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor - handle 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('recoverai_token');
      localStorage.removeItem('recoverai_user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// Auth
export const authApi = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  me: () => api.get('/auth/me'),
  logout: () => api.post('/auth/logout'),
};

// Dashboard
export const dashboardApi = {
  summary: () => api.get('/dashboard/summary'),
  trends: () => api.get('/dashboard/trends'),
  recentActivity: () => api.get('/dashboard/recent-activity'),
};

// Invoices
export const invoiceApi = {
  list: (params?: Record<string, string | number>) =>
    api.get('/invoices', { params }),
  get: (id: number) => api.get(`/invoices/${id}`),
  analyze: (id: number) => api.post(`/invoices/${id}/analyze`),
  draftReminder: (id: number, message?: string) =>
    api.post(`/invoices/${id}/actions/draft-reminder`, { message }),
  sendReminder: (id: number, message: string, idempotencyKey: string) =>
    api.post(`/invoices/${id}/actions/send-reminder`, {
      message,
      idempotency_key: idempotencyKey,
    }),
  escalate: (id: number, reason: string) =>
    api.post(`/invoices/${id}/actions/escalate`, { reason }),
  markPaid: (id: number) => api.post(`/invoices/${id}/mark-paid`),
  addNote: (id: number, content: string) =>
    api.post(`/invoices/${id}/notes`, { content }),
};

// Customers
export const customerApi = {
  list: (params?: Record<string, string>) =>
    api.get('/customers', { params }),
  get: (id: number) => api.get(`/customers/${id}`),
};

// Analytics
export const analyticsApi = {
  overview: () => api.get('/analytics/overview'),
  bySegment: () => api.get('/analytics/recovery-by-segment'),
  byAge: () => api.get('/analytics/recovery-by-age'),
};

// Audit
export const auditApi = {
  list: (params?: Record<string, string | number>) =>
    api.get('/audit-logs', { params }),
};

// Settings
export const settingsApi = {
  get: () => api.get('/settings'),
  update: (data: Record<string, string>) => api.put('/settings', data),
};
