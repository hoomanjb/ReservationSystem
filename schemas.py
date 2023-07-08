from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ListingResponse(BaseModel):
    id: int
    name: str
    description: str = Field(default=None, title='Description')

    class Config:
        orm_mode = True


class ListingCreate(BaseModel):
    name: str = Field(title='List Name')
    description: str = Field(default=None, title='Description')


class RoomResponse(BaseModel):
    id: int
    listing_id: int
    name: str

    class Config:
        orm_mode = True


class RoomCreate(BaseModel):
    name: str = Field(title='Room Name')
    listing_id: int = Field(title='Listing ID')


class ReservationCreate(BaseModel):
    room_id: int
    name: str
    start_time: datetime
    end_time: datetime  # for test "2023-08-12 12:22"


class ReservationResponse(BaseModel):
    id: int
    room_id: int
    name: str
    start_time: datetime
    end_time: datetime
    user_id: int

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
