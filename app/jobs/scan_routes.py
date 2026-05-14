"""Job to scan all monitored routes for flight deals"""

import logging
from datetime import datetime, timedelta
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models.route import Route
from app.models.price_snapshot import PriceSnapshot
from app.scrapers.kiwi import KiwiScraper
from app.engines.price_engine import save_snapshot_if_deal
from app.engines.alert_router import AlertRouter

logger = logging.getLogger(__name__)


async def scan_all_routes() -> dict:
    """
    Scan all active monitored routes for flight deals.
    
    Process:
    1. Get all active routes from database
    2. For each route, search flights with 90-day window
    3. Save snapshots if they're deals
    4. Route deals to free group and paid users
    
    Returns:
        Dictionary with scan results
    """
    result = {
        "routes_scanned": 0,
        "deals_found": 0,
        "alerts_sent": 0,
        "errors": [],
    }
    
    if AsyncSessionLocal is None:
        result["errors"].append("Database not initialized")
        logger.error("Database not initialized")
        return result
    
    scraper = KiwiScraper()
    router = AlertRouter()
    
    async with AsyncSessionLocal() as db:
        try:
            # Get all active routes
            stmt = select(Route).where(Route.is_active == True)
            routes_result = await db.execute(stmt)
            routes = routes_result.scalars().all()
            
            logger.info(f"Scanning {len(routes)} routes")
            
            for route in routes:
                try:
                    result["routes_scanned"] += 1
                    
                    # Build search dates (next 90 days)
                    today = datetime.utcnow()
                    date_from = today.strftime("%d/%m/%Y")
                    date_to = (today + timedelta(days=90)).strftime("%d/%m/%Y")
                    
                    # Search for flights
                    flights = await scraper.search_route(
                        fly_from=route.origin_iata,
                        fly_to=route.destination_iata,
                        date_from=date_from,
                        date_to=date_to,
                        limit=10,
                    )
                    
                    logger.info(f"Found {len(flights)} flights for {route.origin_iata}->{route.destination_iata}")
                    
                    # Process each flight
                    for flight in flights:
                        try:
                            # Build snapshot data
                            snapshot_data = {
                                "origin": flight.get("origin"),
                                "destination": flight.get("destination"),
                                "price": flight.get("price"),
                                "currency": flight.get("currency", "BRL"),
                                "airline": flight.get("airline"),
                                "airline_iata": flight.get("airline_iata"),
                                "departure_at": flight.get("departure_at"),
                                "return_at": flight.get("return_at"),
                                "duration_minutes": flight.get("duration_minutes"),
                                "booking_url": flight.get("booking_url"),
                                "deep_link": flight.get("deep_link"),
                            }
                            
                            # Save if deal
                            snapshot = await save_snapshot_if_deal(db, snapshot_data, route)
                            
                            if snapshot:
                                result["deals_found"] += 1
                                
                                # Route the deal
                                route_result = await router.route_deal(db, snapshot)
                                result["alerts_sent"] += route_result["users_notified"]
                                
                                if route_result["errors"]:
                                    result["errors"].extend(route_result["errors"])
                        
                        except Exception as e:
                            logger.error(f"Error processing flight: {e}")
                            result["errors"].append(f"Flight processing: {str(e)}")
                
                except Exception as e:
                    logger.error(f"Error scanning route {route.origin_iata}->{route.destination_iata}: {e}")
                    result["errors"].append(f"Route {route.origin_iata}->{route.destination_iata}: {str(e)}")
            
            await db.commit()
        
        except Exception as e:
            logger.error(f"Error in scan_all_routes: {e}")
            result["errors"].append(f"Scan: {str(e)}")
    
    logger.info(f"Scan complete: {result['routes_scanned']} routes, {result['deals_found']} deals, {result['alerts_sent']} alerts sent")
    return result
