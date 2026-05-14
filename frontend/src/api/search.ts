import { apiClient } from './client';

export interface Deal {
  origin: string;
  destination: string;
  origin_city: string;
  origin_country: string;
  destination_city: string;
  destination_country: string;
  price: number;
  currency: string;
  airline: string;
  airline_iata: string;
  airline_logo_url: string;
  departure_at: string;
  return_at?: string;
  duration_minutes: number;
  stops: number;
  booking_url: string;
  deep_link: string;
  is_deal: boolean;
  deal_badge?: string;
}

export interface SearchParams {
  fly_from: string;
  fly_to?: string;
  date_from?: string;
  date_to?: string;
  max_price?: number;
  trip_type?: 'oneway' | 'roundtrip';
  nights_min?: number;
  nights_max?: number;
  adults?: number;
  limit?: number;
}

export interface SearchResponse {
  results: Deal[];
  total: number;
  search_meta: {
    fly_from: string;
    fly_to: string;
    searched_at: string;
    source: string;
  };
}

export const searchAPI = {
  searchDeals: async (params: SearchParams): Promise<SearchResponse> => {
    const response = await apiClient.get<SearchResponse>('/api/search/deals', {
      params,
    });
    return response.data;
  },

  previewMatch: async (
    userId: string,
    deals: Deal[]
  ): Promise<{
    user: { id: string; name: string; plan: string };
    matched_deals: Deal[];
    matched_alerts: Array<{
      id: string;
      origin_iata?: string;
      destination_iata?: string;
      matched_deal_count: number;
    }>;
    unmatched_count: number;
    active_alerts: number;
  }> => {
    const response = await apiClient.post('/api/search/preview-match', {
      user_id: userId,
      deals,
    });
    return response.data;
  },
};
