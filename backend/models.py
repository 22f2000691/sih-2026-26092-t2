from sqlalchemy import Column, Integer, String, Float, Boolean
from geoalchemy2 import Geometry

try:
    from database import Base, DATABASE_URL
except ModuleNotFoundError:
    from .database import Base, DATABASE_URL

class ChannelPartner(Base):
    __tablename__ = "channel_partners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    partner_type = Column(String) # E.g., SCA, PSB, RRB
    npa_ratio = Column(Float, default=0.0)
    active_quota = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    
    # Point geometry for geospatial routing (Longitude, Latitude)[cite: 1]
    location = Column(String) if DATABASE_URL.startswith("sqlite") else Column(Geometry(geometry_type='POINT', srid=4326, spatial_index=True))
