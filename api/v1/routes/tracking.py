from fastapi import Depends, APIRouter, Request, status, Query, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
 


from api.utils.success_response import success_response
from api.db.database import get_db
from api.v1.models.tracking import DeliveryUpdate
from api.v1.schemas.tracking import TrackingBase, TrackingUpdate
from api.v1.services.tracking import tracking_services


track_router = APIRouter(prefix="/tracking", tags=["Tracking"])

@track_router.post("/")
def create_tracking(schema: TrackingBase, db:Session = Depends(get_db)):
    """Endpoint to create tracking details"""
    tracking = tracking_services.create(db=db, schema=schema)

    return tracking

@track_router.get("/")
def get_tracking(db:Session = Depends(get_db)):
    '''Endpoint to get tracking details'''
    tracking = tracking_services.fetch_all(db=db)
    if not tracking:
        raise HTTPException(status_code=404, detail="Update Not Found")
    return tracking

@track_router.get("/{track_number}")
def get_single_tracking(track_number:str, db:Session= Depends(get_db), ):
    tracking=tracking_services.fetch(db=db, tracking_number=track_number)
    if not tracking:
        raise HTTPException(status_code=404, detail="Update Not Found")
    
    return jsonable_encoder(tracking)




@track_router.post("/update")
def update_tracking(schema: TrackingUpdate, db:Session = Depends(get_db)):
    """Endpoint to update tracking details"""
    tracking = tracking_services.update(db=db, schema=schema)
    if not tracking:
        raise HTTPException(status_code=404, detail="Update Not Found")
    
    return tracking

@track_router.get("/delivery-update/{update_id}")
def get_update(update_id: str, db: Session = Depends (get_db)):
    track = tracking_services.get_single_update(update_id=update_id, db=db)
    if not track:
        raise HTTPException(status_code=404, detail="Update Not Found")
    
    return track
    
