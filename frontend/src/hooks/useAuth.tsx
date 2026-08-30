import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User } from '../types';
import { authApi } from '../services/api';

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isManager: boolean;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('recoverai_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      authApi.me()
        .then((res) => setUser(res.data.user))
        .catch(() => {
          localStorage.removeItem('recoverai_token');
          localStorage.removeItem('recoverai_user');
          setToken(null);
          setUser(null);
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [token]);

  const login = async (email: string, password: string) => {
    const res = await authApi.login(email, password);
    const { token: newToken, user: newUser } = res.data;
    localStorage.setItem('recoverai_token', newToken);
    localStorage.setItem('recoverai_user', JSON.stringify(newUser));
    setToken(newToken);
    setUser(newUser);
  };

  const logout = () => {
    authApi.logout().catch(() => {});
    localStorage.removeItem('recoverai_token');
    localStorage.removeItem('recoverai_user');
    setToken(null);
    setUser(null);
  };

  const isManager = user?.role === 'finance_manager';

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isManager, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
