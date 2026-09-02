from sqlalchemy import Column, Integer, String, Float, Boolean
from geoalchemy2 import Geometry

try:
    from database import Base
except ModuleNotFoundError:
    from .database import Base

class ChannelPartner(Base):
    __tablename__ = "channel_partners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    partner_type = Column(String) # E.g., SCA, PSB, RRB
    npa_ratio = Column(Float, default=0.0)
    active_quota = Column(Float, default=0.0)
    supported_schemes = Column(String, default="")
    overdue_ratio = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    
    # Point geometry for geospatial routing (Longitude, Latitude)[cite: 1]
    location = Column(Geometry(geometry_type='POINT', srid=4326, spatial_index=True))
