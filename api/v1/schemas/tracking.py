import re
from datetime import datetime
from typing import Optional, Union, List

from pydantic import BaseModel, EmailStr, field_validator, ConfigDict, Field



class TrackingBase(BaseModel):
    """Base schema for users"""
        
    senders_name : str
    senders_email :EmailStr    
    senders_phonenumber :str
    package :str
    additional_desc :str
    address_to :str
    pickup_loc:str
    product_picture :str
    officer_ondeck:str
    reciever_name:str
    reciever_email: EmailStr
    reciever_phonenumber :str
    price :float
   

    model_config = ConfigDict(from_attributes=True)


class TrackingUpdate(BaseModel):
    """tracking updates"""
    id:str   
    senders_name : Optional[str]
    senders_email :Optional[EmailStr]    
    senders_phonenumber :Optional[str]
    package :Optional[str]
    additional_desc :Optional[str]
    address_to :Optional[str]
    pickup_loc:Optional[str]
    product_picture :Optional[str]
    reciever_name:Optional[str]
    reciever_email: Optional[EmailStr]
    reciever_phonenumber :Optional[str]

   

    model_config = ConfigDict(from_attributes=True)

class DeliveryUpdateS(BaseModel):

    tracking_id: str
    status: str
    location: str
    remarks: str

