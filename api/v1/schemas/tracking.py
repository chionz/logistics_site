import re
from datetime import datetime
from typing import Optional, Union, List

from pydantic import BaseModel, EmailStr, field_validator, ConfigDict, Field


class TrackingBase(BaseModel):
    senders_name: str
    senders_email: Optional[EmailStr] = None
    senders_phonenumber: Optional[str] = None
    package: str
    additional_desc: Optional[str] = None
    address_to: str
    pickup_loc: str
    product_picture: Optional[str] = None
    officer_ondeck: Optional[str] = None
    status: Optional[str] = "pending"  # Optional, default is "pending"
    reciever_name: str
    reciever_email: Optional[EmailStr] = None
    reciever_phonenumber: Optional[str] = None
    price: float

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
