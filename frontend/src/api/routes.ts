import { apiClient } from './client';

export interface Route {
  id: string;
  origin_iata: string;
  destination_iata: string;
  threshold_price: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export const routesAPI = {
  listRoutes: async (): Promise<Route[]> => {
    const response = await apiClient.get<Route[]>('/api/routes');
    return response.data;
  },

  getRoute: async (routeId: string): Promise<Route> => {
    const response = await apiClient.get<Route>(`/api/routes/${routeId}`);
    return response.data;
  },

  createRoute: async (data: {
    origin_iata: string;
    destination_iata: string;
    threshold_price: number;
  }): Promise<Route> => {
    const response = await apiClient.post<Route>('/api/routes', data);
    return response.data;
  },

  updateRoute: async (routeId: string, data: Partial<Route>): Promise<Route> => {
    const response = await apiClient.put<Route>(`/api/routes/${routeId}`, data);
    return response.data;
  },

  deleteRoute: async (routeId: string): Promise<void> => {
    await apiClient.delete(`/api/routes/${routeId}`);
  },
};
