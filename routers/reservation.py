from typing import List

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from database.database_base import get_db
from database.models import Reservation
from oauth2 import get_current_user
from schemas import ReservationCreate, ReservationResponse

router = APIRouter(prefix='/reservation', tags=['Reservation'])


@router.get("/", response_model=List[ReservationResponse])
async def get_reservations(db: Session = Depends(get_db),
                           user_id: int = Depends(get_current_user),
                           limit: int = 10, skip: int = 0):
    reservations_db = db.query(Reservation).limit(limit).offset(skip).all()
    if not reservations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Reservations Not found"
        )
    return reservations_db


@router.get("/{id}", response_model=ReservationResponse)
async def get_reservation(reservation_id: int, db: Session = Depends(get_db),
                          user_id: int = Depends(get_current_user)):
    reservation = db.query(
        Reservation).filter(Reservation.user_id == user_id).filter(Reservation.id == reservation_id).one_or_none()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"reservation_id {reservation_id} Not found"
        )
    if user_id != reservation.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')
    return reservation


@router.post("/", status_code=status.HTTP_201_CREATED)
async def make_reservation(reservation: ReservationCreate,
                           user_id: int = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    new_reservation = Reservation(
        room_id=reservation.room_id, name=reservation.name,
        start_time=reservation.start_time, end_time=reservation.end_time, user_id=user_id)
    # new_reservation = Reservation(**reservation.dict())
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return {'data': new_reservation, 'message': 'Reservation created successfully'}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(
        reservation_id: int, db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reservation {reservation_id} Not found")
    if user_id != reservation.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')
    reservation.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
async def update_reservation(
        reservation_id: int, reservation: ReservationCreate, db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)):
    my_reservation = db.query(Reservation).filter(Reservation.id == reservation_id)
    pre_reservation = my_reservation.first()
    if pre_reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reservation {reservation_id} Not found")
    my_reservation.update(reservation.dict(), synchronize_session=False)
    db.commit()
    return {'message': 'Reservation updated'}
