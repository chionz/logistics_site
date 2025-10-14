import random
import string
from typing import Any, Optional, Annotated
from fastapi import Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session, joinedload


from api.core.base.services import Service
from api.core.dependencies.email_sender import send_email
from api.db.database import get_db
from api.v1.models.tracking import DeliveryUpdate, Tracking
from api.v1.schemas import user
from api.v1.schemas.tracking import DeliveryUpdateS, TrackingBase, TrackingUpdate


class TrackService(Service):
    """User service"""

    def fetch_all(self,db:Session):
        track = db.query(Tracking).all()
        return {"message":"successfully fetched all Tracking","Data":track}

    def fetch(self,db:Session,tracking_number):
        tracking = db.query(Tracking).options(joinedload(Tracking.updates)).filter(Tracking.id == tracking_number).first()
        #tracking= db.query(Tracking).filter(Tracking.id==tracking_number).first()
        if tracking == None:
            raise HTTPException(
                                status_code=404,
                                detail="Not Found"
                                )
        
        return{"message":"successfully fetched tracking number",
               "data":tracking,
               "food": "akpu"
               }

    def delete():
        pass
    
    def update(self,db:Session, schema: TrackingUpdate):
        """"""
        tracking= db.query(Tracking).filter(Tracking.id==schema.id).first()
        if tracking ==None:
            raise HTTPException(
                                status_code=404,
                                detail="Not Found"
                                )
        # Automatically update fields from schema to model
        update_data = schema.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(tracking, key, value)

        db.commit()
        db.refresh(tracking)
        return{
                "message": "successfully updated",
                "data":tracking
            }

   
    def create(self, db: Session, schema: TrackingBase):
        """Creates a tracking details"""

        tracking = db.query(Tracking).all()

        # Create tracking details and other attributes from schema
        track =Tracking(**schema.model_dump())
        db.add(track)
        db.commit()
        db.refresh(track) 

        return {
            "message": "Created successfully",
            "data": track
        }
    
    def create_delivery_update(self, db: Session, schema: DeliveryUpdateS):
        """Creates a tracking details"""

        # Create tracking details and other attributes from schema
        delivery =DeliveryUpdate(**schema.model_dump())
        db.add(delivery)
        db.commit()
        db.refresh(delivery) 

        return {
            "message": "Created successfully",
            "data": delivery
        }
    

    def get_single_update(self, update_id: str, db:Session):
        track=db.query(DeliveryUpdate).filter(DeliveryUpdate.id == update_id).first()
        if not track:
            raise HTTPException(
                                status_code=404,
                                detail="Not Found"
                                )
        
        return{"message": "update successfully found",
                   "data": track}
    
tracking_services=TrackService()

