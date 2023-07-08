from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from schemas import ListingResponse, ListingCreate
from database.database_base import get_db
from database.models import Listing
from oauth2 import get_current_user

router = APIRouter(prefix='/listings', tags=['Listings'])


@router.get("/", response_model=List[ListingResponse])
async def get_listings(db: Session = Depends(get_db),
                       user_id: int = Depends(get_current_user),
                       limit: int = 10, skip: int = 0):
    listings_db = db.query(Listing).limit(limit).offset(skip).all()
    if not listings_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"listings Not found"
        )
    return listings_db


@router.get("/{listing_id}", response_model=ListingResponse)
async def get_listing(listing_id: int, db: Session = Depends(get_db),
                      user_id: int = Depends(get_current_user)):
    listing = db.query(Listing).filter(Listing.user_id == user_id).filter(Listing.id == listing_id).one_or_none()
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"listing_id {listing_id} Not found"
        )
    if user_id != listing.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')
    return listing


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_listing(
        listing: ListingCreate, db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)):
    new_listing = Listing(name=listing.name, description=listing.description, user_id=user_id)
    # new_listing = Listing(**listing.dict())
    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)
    return {'data': new_listing, 'message': 'Listing Created Successfully'}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_listing(
        listing_id: int, db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)):
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if listing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"listing {listing_id} Not found")
    if user_id != listing.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')
    listing.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
async def update_listing(
        listing_id: int, listing: ListingCreate, db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)):
    my_listing = db.query(Listing).filter(Listing.id == listing_id)
    pre_listing = my_listing.first()
    if pre_listing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Listing {listing_id} Not found")
    if user_id != pre_listing.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')
    my_listing.update(listing.dict(), synchronize_session=False)
    db.commit()
    return {'message': 'listing updated'}
