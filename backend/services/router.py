from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.shape import to_shape

try:
    import models
    from schemas import LoanApplicationRequest
except ModuleNotFoundError:
    from .. import models
    from ..schemas import LoanApplicationRequest

def find_optimal_partners(db: Session, request: LoanApplicationRequest, radius_km: float = 25.0):
    # Convert user lat/lon into a PostGIS Point (SRID 4326 for GPS coordinates)
    user_point = f"POINT({request.longitude} {request.latitude})"
    
    # Calculate a simple health score: (Active Quota / (NPA Ratio + 1))
    # Higher active quota and lower NPA yields a better score
    health_score = models.ChannelPartner.active_quota / (models.ChannelPartner.npa_ratio + models.ChannelPartner.overdue_ratio + 1)
    requested_scheme = "Education Loan" if request.education_status or request.business_type == "Education" else ("Microfinance" if request.capital_required <= 140000 else "Term Loan")
    
    # Query for active partners within the radius (in meters), ordered by health score then distance
    optimal_partners = db.query(
        models.ChannelPartner,
        func.ST_DistanceSphere(models.ChannelPartner.location, func.ST_GeomFromText(user_point, 4326)).label("distance_meters")
    ).filter(
        models.ChannelPartner.is_active == True,
        models.ChannelPartner.active_quota >= request.capital_required * 0.90,
        models.ChannelPartner.npa_ratio < 5.0,
        models.ChannelPartner.overdue_ratio < 5.0,
        models.ChannelPartner.supported_schemes.ilike(f"%{requested_scheme}%"),
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
        point = to_shape(partner.location)
        results.append({
            "partner_id": partner.id,
            "name": partner.name,
            "type": partner.partner_type,
            "distance_km": round(distance / 1000, 2),
            "health_status": "Healthy",
            "remaining_capacity": partner.active_quota,
            "supported_schemes": [item.strip() for item in partner.supported_schemes.split(",") if item.strip()],
            "latitude": point.y,
            "longitude": point.x,
        })
        
    return results
