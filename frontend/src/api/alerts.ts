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

interface AlertListResponse {
  total: number;
  alerts: UserAlert[];
}

export const alertsAPI = {
  listAlerts: async (userId?: string): Promise<UserAlert[]> => {
    const response = await apiClient.get<AlertListResponse>('/api/alerts', {
      params: userId ? { user_id: userId } : {},
    });
    return response.data.alerts;
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
    const response = await apiClient.post<UserAlert>(
      '/api/alerts',
      {
        origin_iata: data.origin_iata,
        destination_iata: data.destination_iata,
        date_from: data.date_from,
        date_to: data.date_to,
        max_price: data.max_price,
      },
      {
        params: { user_id: data.user_id },
      }
    );
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
