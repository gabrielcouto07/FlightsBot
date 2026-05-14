import { apiClient } from './client';

export interface DemoSeedResponse {
  message: string;
  counts: {
    users_created: number;
    routes_created: number;
    alerts_created: number;
  };
}

export interface DemoNotification {
  id: string;
  user_name: string;
  user_plan: string;
  deal_summary: string;
  triggered_at: string;
}

export interface DemoNotificationsResponse {
  notifications: DemoNotification[];
  total: number;
}

export const demoAPI = {
  seedData: async (): Promise<DemoSeedResponse> => {
    const response = await apiClient.post<DemoSeedResponse>('/api/demo/seed');
    return response.data;
  },

  getNotifications: async (limit: number = 50): Promise<DemoNotificationsResponse> => {
    const response = await apiClient.get<DemoNotificationsResponse>('/api/demo/notifications', {
      params: { limit },
    });
    return response.data;
  },
};
