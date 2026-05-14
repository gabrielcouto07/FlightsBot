import { apiClient } from './client';

export interface User {
  id: string;
  phone_number: string;
  name?: string;
  plan: 'free' | 'paid';
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export const usersAPI = {
  listUsers: async (): Promise<User[]> => {
    const response = await apiClient.get<User[]>('/api/users');
    return response.data;
  },

  getUser: async (userId: string): Promise<User> => {
    const response = await apiClient.get<User>(`/api/users/${userId}`);
    return response.data;
  },

  createUser: async (data: {
    phone_number: string;
    name?: string;
    plan: 'free' | 'paid';
  }): Promise<User> => {
    const response = await apiClient.post<User>('/api/users', data);
    return response.data;
  },

  updateUser: async (userId: string, data: Partial<User>): Promise<User> => {
    const response = await apiClient.put<User>(`/api/users/${userId}`, data);
    return response.data;
  },

  deleteUser: async (userId: string): Promise<void> => {
    await apiClient.delete(`/api/users/${userId}`);
  },
};
