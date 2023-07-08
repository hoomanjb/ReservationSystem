from datetime import datetime

from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session

from database.database_base import get_db
from database.models import Room, Reservation, Listing

router = APIRouter(prefix='/report', tags=['Report'])


@router.get("/availability", status_code=status.HTTP_200_OK)
async def check_availability(
        start_time: datetime, end_time: datetime, db: Session = Depends(get_db)):
    reserved_room_id = db.query(Reservation.room_id).filter(
        Reservation.start_time < end_time).filter(
        Reservation.end_time > start_time).all()
    rooms = db.query(Room.id).all()
    result = [item[0] for item in rooms]
    if reserved_room_id:
        for room_id in reserved_room_id:
            for room in rooms:
                if room == room_id and room[0] in result:
                    result.remove(room[0])
                    break
    if not result:
        return {'message': 'All Rooms are Reserved'}
    return {'rooms': result, 'message': 'All Room-ID that Available'}


@router.get("/overview")
async def get_overview_report(db: Session = Depends(get_db)):
    reservations_db = db.query(Reservation).all()
    rooms_db = db.query(Room).all()
    listings_db = db.query(Listing).all()
    result = []
    for reservation in reservations_db:
        room = next((room for room in rooms_db if room.id == reservation.room_id), None)
        listing = next((listing for listing in listings_db if listing.id == room.listing_id), None)
        report = f"Listing: {listing.name} | Room: {room.name} | Reservation: {reservation.name} | Start Time: {reservation.start_time} | End Time: {reservation.end_time}\n"
        result.append(report)
    return result
