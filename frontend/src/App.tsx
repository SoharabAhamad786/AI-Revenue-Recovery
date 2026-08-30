import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './hooks/useAuth';
import { ThreeDProvider } from './3d/ThreeDContext';
import './3d/threeDStyles.css';
import AppLayout from './layouts/AppLayout';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import RecoveryQueuePage from './pages/RecoveryQueuePage';
import InvoiceDetailPage from './pages/InvoiceDetailPage';
import CustomersPage from './pages/CustomersPage';
import AnalyticsPage from './pages/AnalyticsPage';
import AuditLogPage from './pages/AuditLogPage';
import SettingsPage from './pages/SettingsPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, loading } = useAuth();
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
      </div>
    );
  }
  if (!user) return <Navigate to="/login" replace />;
  return <>{children}</>;
};

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <ThreeDProvider>
            <Toaster
              position="top-right"
              toastOptions={{
                duration: 4000,
                style: { fontSize: '14px' },
              }}
            />
            <Routes>
              <Route path="/login" element={<LoginPage />} />
              <Route
                element={
                  <ProtectedRoute>
                    <AppLayout />
                  </ProtectedRoute>
                }
              >
                <Route path="/" element={<DashboardPage />} />
                <Route path="/recovery-queue" element={<RecoveryQueuePage />} />
                <Route path="/invoices/:id" element={<InvoiceDetailPage />} />
                <Route path="/customers" element={<CustomersPage />} />
                <Route path="/analytics" element={<AnalyticsPage />} />
                <Route path="/audit-log" element={<AuditLogPage />} />
                <Route path="/settings" element={<SettingsPage />} />
              </Route>
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </ThreeDProvider>
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
};

export default App;
