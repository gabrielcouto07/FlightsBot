import { apiClient } from './client';

export interface UserAlert {
  id: string;
  user_id: string;
  origin_iata?: string;
  destination_iata?: string;
  date_from?: string;
  date_to?: string;
  max_price: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export const alertsAPI = {
  listAlerts: async (userId?: string): Promise<UserAlert[]> => {
    const response = await apiClient.get<UserAlert[]>('/api/alerts', {
      params: userId ? { user_id: userId } : {},
    });
    return response.data;
  },

  getAlert: async (alertId: string): Promise<UserAlert> => {
    const response = await apiClient.get<UserAlert>(`/api/alerts/${alertId}`);
    return response.data;
  },

  createAlert: async (data: {
    user_id: string;
    origin_iata?: string;
    destination_iata?: string;
    date_from?: string;
    date_to?: string;
    max_price: number;
  }): Promise<UserAlert> => {
    const response = await apiClient.post<UserAlert>('/api/alerts', data);
    return response.data;
  },

  updateAlert: async (alertId: string, data: Partial<UserAlert>): Promise<UserAlert> => {
    const response = await apiClient.put<UserAlert>(`/api/alerts/${alertId}`, data);
    return response.data;
  },

  deleteAlert: async (alertId: string): Promise<void> => {
    await apiClient.delete(`/api/alerts/${alertId}`);
  },
};
