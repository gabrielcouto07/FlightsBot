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
  booking_token?: string;
  deeplink_url: string;
  booking_source: 'kiwi' | 'direct_airline' | 'google_flights' | 'airline_homepage';
  booking_source_label: string;
  provider_code: string;
  booking_url: string;
  deep_link: string;
  provider_name: string;
  booking_source_type: string;
  deeplink_tier: number;
  provider_itinerary_id?: string;
  fare_token?: string;
  fare_last_seen_at: string;
  purchase_url: string;
  purchase_label: string;
  secondary_purchase_url: string;
  secondary_purchase_label: string;
  official_airline_url: string;
  official_airline_label: string;
  historical_avg_price: number;
  historical_low_price: number;
  savings_percent: number;
  trend_change_7d: number;
  price_history_7d: number[];
  opportunity_score: number;
  opportunity_badges: string[];
  distance_miles?: number;
  cpm?: number;
  is_deal: boolean;
  deal_badge?: string;
}

export interface AirportOption {
  code: string;
  city: string;
  country: string;
  flag: string;
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
  airline?: string;
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
    actionable_link_rate: number;
    source_confidence_note: string;
  };
  kpis: {
    total_scanned_24h: number;
    active_alerts: number;
    average_cpm?: number | null;
    top_saving_percent: number;
  };
}

export const searchAPI = {
  searchDeals: async (params: SearchParams): Promise<SearchResponse> => {
    const response = await apiClient.get<SearchResponse>('/api/search/deals', {
      params,
    });
    return response.data;
  },

  listAirports: async (): Promise<AirportOption[]> => {
    const response = await apiClient.get<AirportOption[]>('/api/search/airports');
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
