import random
import string
from typing import Any, Optional, Annotated
from fastapi import Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session


from api.core.base.services import Service
from api.core.dependencies.email_sender import send_email
from api.db.database import get_db
from api.v1.models.tracking import Tracking
from api.v1.schemas import user
from api.v1.schemas.tracking import TrackingBase


class TrackService(Service):
    """User service"""

    def fetch_all(self,db:Session):
        track = db.query(Tracking).all()
        return {"message":"successfully fetched all Tracking","Data":track}

    def fetch():
        pass

    def delete():
        pass
    
    def update(self,db:Session, schema: TrackingBase):
        """"""
        tracking= db.query(Tracking).filter(Tracking.tracking_number==schema.tracking_number).first()
        if tracking ==None:
            return"not found"
        else:
            tracking.price = schema.price
            tracking.dispatch_location=schema.dispatch_location
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
    
tracking_services=TrackService()

