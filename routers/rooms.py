from typing import List

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from database.database_base import get_db
from database.models import Room
from oauth2 import get_current_user
from schemas import RoomResponse, RoomCreate

router = APIRouter(prefix='/rooms', tags=['Rooms'])


@router.get("/", response_model=List[RoomResponse])
async def get_rooms(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    rooms_db = db.query(Room).all()
    if not rooms_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"rooms Not found"
        )
    return rooms_db


@router.get("/{id}", response_model=RoomResponse)
async def get_room(room_id: int, db: Session = Depends(get_db),
                    user_id: int = Depends(get_current_user)):

    room = db.query(Room).filter(Room.id == room_id).one_or_none()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"room_id {room_id} Not found"
        )
    return room


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_room(
        room: RoomCreate, db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)):
    new_room = Room(name=room.name, listing_id=room.listing_id)
    # new_room = Room(**room.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return {'data': new_room, 'message': 'Room Created Successfully'}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
        room_id: int, db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"room {room} Not found")
    room.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
async def update_room(
        room_id: int, room: RoomCreate, db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)):
    my_room = db.query(Room).filter(Room.id == room_id)
    pre_room = my_room.first()
    if pre_room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"room {room_id} Not found")
    my_room.update(room.dict(), synchronize_session=False)
    db.commit()
    return {'message': 'room updated'}
