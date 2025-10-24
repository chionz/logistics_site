""" tracking data models
"""

from sqlalchemy import Column, String, Float, Boolean, text, ForeignKey
from sqlalchemy.orm import relationship
from api.v1.models.base_model import BaseTableModel
from api.db.database import Base


class Tracking(BaseTableModel):
    __tablename__ = "tracking"

    senders_name = Column(String, unique=False, nullable=False)
    senders_email = Column(String, nullable=True)
    senders_phonenumber = Column(String, nullable=True)
    package = Column(String, nullable=False)

    additional_desc = Column(String, nullable=True)
    address_to = Column(String, nullable=False)  
    pickup_loc = Column(String, nullable=False)
    product_picture = Column(String, nullable=True)

    officer_ondeck=Column(String,nullable=True)
    status = Column(String,nullable=False,server_default="pending")
    reciever_name=Column(String,nullable=False)
    reciever_email = Column(String, nullable=True)
    reciever_phonenumber = Column(String, nullable=True)

    is_deleted = Column(Boolean, server_default=text("false"))

    price = Column(Float, nullable=False)
    updates = relationship("DeliveryUpdate", back_populates="tracking", cascade="all, delete-orphan")
   


    # new class
class DeliveryUpdate(BaseTableModel):
    __tablename__ = "delivery_updates"

    tracking_id = Column(String, ForeignKey("tracking.id"), nullable=False)

    status = Column(String, nullable=False)
    location = Column(String, nullable=True)
    remarks = Column(String, nullable=True)
    is_deleted = Column(Boolean, server_default=text("false"))

    tracking = relationship("Tracking", back_populates="updates")
