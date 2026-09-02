from database import SessionLocal
from models import ChannelPartner

def seed_data():
    db = SessionLocal()
    
    # Clear existing data for a clean test environment
    db.query(ChannelPartner).delete()
    
    partners = [
        # 1. Optimal Partner: Close by, high active quota, low NPA (Healthy)
        ChannelPartner(
            name="Assam Gramin Vikash Bank - Main Branch",
            partner_type="RRB",
            npa_ratio=2.1,
            active_quota=5000000.0,
            supported_schemes="Microfinance,Term Loan,Education Loan",
            overdue_ratio=1.0,
            is_active=True,
            # Note: PostGIS expects Longitude first, then Latitude
            location="SRID=4326;POINT(91.7362 26.1445)" 
        ),
        # 2. Warning Partner: Close by, but high NPA and lower quota
        ChannelPartner(
            name="State Bank of India - Dispur",
            partner_type="PSB",
            npa_ratio=8.5, 
            active_quota=1000000.0,
            supported_schemes="Microfinance,Term Loan",
            overdue_ratio=6.0,
            is_active=True,
            location="SRID=4326;POINT(91.7923 26.1433)" # ~5 km distance
        ),
        # 3. Out of Range Partner: Good stats, but > 25km away[cite: 1]
        ChannelPartner(
            name="Assam Cooperative Apex Bank - Rangia",
            partner_type="SCA",
            npa_ratio=1.5,
            active_quota=4000000.0,
            supported_schemes="Term Loan,Education Loan",
            overdue_ratio=0.5,
            is_active=True,
            location="SRID=4326;POINT(91.6247 26.4358)" # ~35 km distance
        ),
        # 4. Inactive Partner: Close by, but operations currently suspended
        ChannelPartner(
            name="Punjab National Bank - Panbazar",
            partner_type="PSB",
            npa_ratio=4.0,
            active_quota=0.0,
            supported_schemes="Microfinance,Term Loan",
            overdue_ratio=0.0,
            is_active=False,
            location="SRID=4326;POINT(91.7455 26.1852)" # ~4 km distance
        )
    ]
    
    db.add_all(partners)
    db.commit()
    print("Database seeded with test channel partners.")
    db.close()

if __name__ == "__main__":
    seed_data()
