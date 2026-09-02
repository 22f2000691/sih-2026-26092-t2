import math

from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.elements import WKTElement

try:
    import models
    from schemas import LoanApplicationRequest
except ModuleNotFoundError:
    from .. import models
    from ..schemas import LoanApplicationRequest

def find_optimal_partners(db: Session, request: LoanApplicationRequest, radius_km: float = 25.0):
    if db.bind.dialect.name == "sqlite":
        def distance_km(location):
            try:
                point = location.split("POINT(", 1)[1].rstrip(")")
                longitude, latitude = map(float, point.split())
                latitude_delta = math.radians(latitude - request.latitude)
                longitude_delta = math.radians(longitude - request.longitude)
                a = math.sin(latitude_delta / 2) ** 2 + math.cos(math.radians(request.latitude)) * math.cos(math.radians(latitude)) * math.sin(longitude_delta / 2) ** 2
                return 6371 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            except (AttributeError, IndexError, ValueError):
                return float("inf")

        matches = []
        for partner in db.query(models.ChannelPartner).filter(models.ChannelPartner.is_active == True).all():
            distance = distance_km(partner.location)
            if distance <= radius_km:
                matches.append((partner, distance))
        matches.sort(key=lambda item: (-(item[0].active_quota / (item[0].npa_ratio + 1)), item[1]))
        return [{"partner_id": partner.id, "name": partner.name, "type": partner.partner_type, "distance_km": round(distance, 2), "health_status": "Healthy" if partner.npa_ratio < 5.0 else "Warning"} for partner, distance in matches[:3]]

    # Convert user lat/lon into a PostGIS Point (SRID 4326 for GPS coordinates)
    user_point = f"POINT({request.longitude} {request.latitude})"
    
    # Calculate a simple health score: (Active Quota / (NPA Ratio + 1))
    # Higher active quota and lower NPA yields a better score
    health_score = models.ChannelPartner.active_quota / (models.ChannelPartner.npa_ratio + 1)
    
    # Query for active partners within the radius (in meters), ordered by health score then distance
    optimal_partners = db.query(
        models.ChannelPartner,
        func.ST_DistanceSphere(models.ChannelPartner.location, func.ST_GeomFromText(user_point, 4326)).label("distance_meters")
    ).filter(
        models.ChannelPartner.is_active == True,
        func.ST_DWithin(
            func.ST_Transform(models.ChannelPartner.location, 3857), 
            func.ST_Transform(func.ST_GeomFromText(user_point, 4326), 3857), 
            radius_km * 1000
        )
    ).order_by(
        health_score.desc(),
        func.ST_DistanceSphere(models.ChannelPartner.location, func.ST_GeomFromText(user_point, 4326))
    ).limit(3).all()
    
    # Format the results
    results = []
    for partner, distance in optimal_partners:
        results.append({
            "partner_id": partner.id,
            "name": partner.name,
            "type": partner.partner_type,
            "distance_km": round(distance / 1000, 2),
            "health_status": "Healthy" if partner.npa_ratio < 5.0 else "Warning"
        })
        
    return results
