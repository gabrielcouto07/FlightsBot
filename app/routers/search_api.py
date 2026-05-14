"""Flight search API - search deals and preview user matches"""

import logging
from datetime import datetime, timedelta, date
from typing import Optional
from fastapi import APIRouter, Query, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.models.user_alert import UserAlert
from app.scrapers.kiwi import KiwiScraper
from app.utils.airports import is_domestic, get_airport_info, AIRPORTS
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api/search", tags=["search"])


class DealResponse(BaseModel):
    """Flight deal response schema"""
    origin: str
    destination: str
    origin_city: str
    origin_country: str
    destination_city: str
    destination_country: str
    price: float
    currency: str
    airline: str
    airline_iata: str
    airline_logo_url: str
    departure_at: str
    return_at: Optional[str]
    duration_minutes: int
    stops: int
    booking_url: str
    deep_link: str
    is_deal: bool
    deal_badge: Optional[str] = None


class SearchMetaResponse(BaseModel):
    """Search metadata"""
    fly_from: str
    fly_to: str
    searched_at: str
    source: str


class SearchDealsResponse(BaseModel):
    """Search deals response"""
    results: list[DealResponse]
    total: int
    search_meta: SearchMetaResponse


class MatchedAlert(BaseModel):
    """User alert with match info"""
    id: str
    origin_iata: Optional[str]
    destination_iata: Optional[str]
    date_from: date
    date_to: date
    max_price: float
    matched_deal_count: int


class MatchPreviewResponse(BaseModel):
    """Preview match response"""
    user: dict
    matched_deals: list[DealResponse]
    matched_alerts: list[MatchedAlert]
    unmatched_count: int
    active_alerts: int


@router.get("/deals", response_model=SearchDealsResponse)
async def search_deals(
    fly_from: str = Query(..., description="Origin IATA code (e.g., GRU)"),
    fly_to: str = Query("anywhere", description="Destination IATA code or 'anywhere'"),
    date_from: str = Query(None, description="Start date in YYYY-MM-DD format"),
    date_to: str = Query(None, description="End date in YYYY-MM-DD format"),
    max_price: Optional[float] = Query(None, description="Max price filter"),
    trip_type: str = Query("oneway", description="Trip type: oneway or roundtrip"),
    nights_min: int = Query(3, description="Min nights at destination"),
    nights_max: int = Query(14, description="Max nights at destination"),
    adults: int = Query(1, description="Number of adults"),
    limit: int = Query(20, ge=1, le=50, description="Result limit"),
) -> SearchDealsResponse:
    """
    Search for flight deals.
    
    Returns enriched flight data with pricing tiers, airline logos, and deal badges.
    """
    
    try:
        # Set default dates
        if not date_from:
            date_from = datetime.now().strftime("%Y-%m-%d")
        if not date_to:
            date_to = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
        
        # Convert YYYY-MM-DD to dd/mm/yyyy for Kiwi API
        date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
        date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
        
        date_from_kiwi = date_from_obj.strftime("%d/%m/%Y")
        date_to_kiwi = date_to_obj.strftime("%d/%m/%Y")
        
        scraper = KiwiScraper()
        
        # Search flights
        if fly_to.lower() == "anywhere":
            flights = await scraper.search_anywhere(
                fly_from=fly_from,
                date_from=date_from_kiwi,
                date_to=date_to_kiwi,
                max_price=max_price,
                limit=limit,
            )
        else:
            flights = await scraper.search_route(
                fly_from=fly_from,
                fly_to=fly_to,
                date_from=date_from_kiwi,
                date_to=date_to_kiwi,
                nights_in_dst_from=nights_min,
                nights_in_dst_to=nights_max,
                adults=adults,
                limit=limit,
            )
        
        # Enrich results
        enriched_deals = []
        for flight in flights:
            origin_info = get_airport_info(flight.get("origin", ""))
            dest_info = get_airport_info(flight.get("destination", ""))
            
            is_deal = False
            deal_badge = None
            
            # Determine if it's a deal
            route_is_domestic = is_domestic(flight.get("origin", ""), flight.get("destination", ""))
            threshold = settings.default_threshold_domestic if route_is_domestic else settings.default_threshold_intl
            
            price = flight.get("price", 0)
            if price <= threshold:
                is_deal = True
                deal_badge = "Best price today" if price < threshold * 0.8 else "Good deal"
            
            # Build airline logo URL
            airline_iata = flight.get("airline_iata", "")
            airline_logo_url = f"https://cdn.kiwi.com/airlines/128/{airline_iata.upper()}.png" if airline_iata else ""
            
            deal = DealResponse(
                origin=flight.get("origin", ""),
                destination=flight.get("destination", ""),
                origin_city=origin_info.get("city", ""),
                origin_country=origin_info.get("country", ""),
                destination_city=dest_info.get("city", ""),
                destination_country=dest_info.get("country", ""),
                price=price,
                currency=flight.get("currency", "BRL"),
                airline=flight.get("airline", ""),
                airline_iata=airline_iata,
                airline_logo_url=airline_logo_url,
                departure_at=flight.get("departure_at", ""),
                return_at=flight.get("return_at"),
                duration_minutes=flight.get("duration_minutes", 0),
                stops=flight.get("stops", 0),
                booking_url=flight.get("booking_url", ""),
                deep_link=flight.get("deep_link", ""),
                is_deal=is_deal,
                deal_badge=deal_badge,
            )
            enriched_deals.append(deal)
        
        return SearchDealsResponse(
            results=enriched_deals,
            total=len(enriched_deals),
            search_meta=SearchMetaResponse(
                fly_from=fly_from,
                fly_to=fly_to if fly_to != "anywhere" else "Anywhere",
                searched_at=datetime.now().isoformat(),
                source="kiwi.com",
            ),
        )
    
    except Exception as e:
        logger.error(f"Search error: {e}")
        return SearchDealsResponse(
            results=[],
            total=0,
            search_meta=SearchMetaResponse(
                fly_from=fly_from,
                fly_to=fly_to,
                searched_at=datetime.now().isoformat(),
                source="kiwi.com",
            ),
        )


class PreviewMatchRequest(BaseModel):
    """Request to preview deal matches"""
    user_id: str
    deals: list[DealResponse]


@router.post("/preview-match", response_model=MatchPreviewResponse)
async def preview_match(
    request: PreviewMatchRequest,
    db: AsyncSession = Depends(get_db),
) -> MatchPreviewResponse:
    """
    Preview which deals match a user's active alerts.
    
    Useful for demo purposes to show how alerts work in real-time.
    """
    
    try:
        # Load user
        stmt = select(User).where(User.id == request.user_id)
        user_result = await db.execute(stmt)
        user = user_result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Load user's active alerts
        stmt = select(UserAlert).where(
            (UserAlert.user_id == request.user_id) & (UserAlert.is_active == True)
        )
        alerts_result = await db.execute(stmt)
        alerts = list(alerts_result.scalars().all())
        
        # Match deals against alerts
        matched_deals = []
        matched_alerts_map = {}
        
        for deal in request.deals:
            # Parse deal departure date
            try:
                deal_date = datetime.fromisoformat(deal.departure_at.replace("Z", "+00:00")).date()
            except:
                deal_date = date.today()
            
            for alert in alerts:
                # Check route match
                origin_match = alert.origin_iata is None or alert.origin_iata == deal.origin
                dest_match = alert.destination_iata is None or alert.destination_iata == deal.destination
                
                # Check price match
                price_match = deal.price <= alert.max_price
                
                # Check date match
                date_match = (
                    (alert.date_from is None or deal_date >= alert.date_from) and
                    (alert.date_to is None or deal_date <= alert.date_to)
                )
                
                if origin_match and dest_match and price_match and date_match:
                    matched_deals.append(deal)
                    
                    if alert.id not in matched_alerts_map:
                        matched_alerts_map[alert.id] = {
                            "alert": alert,
                            "count": 0,
                        }
                    matched_alerts_map[alert.id]["count"] += 1
                    break
        
        # Build matched alerts list
        matched_alerts = [
            MatchedAlert(
                id=data["alert"].id,
                origin_iata=data["alert"].origin_iata,
                destination_iata=data["alert"].destination_iata,
                date_from=data["alert"].date_from,
                date_to=data["alert"].date_to,
                max_price=data["alert"].max_price,
                matched_deal_count=data["count"],
            )
            for data in matched_alerts_map.values()
        ]
        
        return MatchPreviewResponse(
            user={
                "id": user.id,
                "name": user.name or "User",
                "plan": user.plan,
            },
            matched_deals=matched_deals,
            matched_alerts=matched_alerts,
            unmatched_count=len(request.deals) - len(matched_deals),
            active_alerts=len(alerts),
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Match preview error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
