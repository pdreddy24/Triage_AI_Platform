from .repository import SessionLocal
from .models import Alert

def create_alert(transaction_id, risk_score, risk_band, route_to):
    db = SessionLocal()
    alert = Alert(
        transaction_id=transaction_id,
        risk_score=risk_score,
        risk_band=risk_band,
        route_to=route_to
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    db.close()
    return alert