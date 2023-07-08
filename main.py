import uvicorn
import structlog as structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import listing, auth, reservation, rooms, report
from database.database_base import engine, Base

logger = structlog.get_logger()
Base.metadata.create_all(bind=engine)
app = FastAPI(title='Reservation System')


origins = [
    "http://localhost",
    "http://localhost:8080",
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(listing.router)
app.include_router(reservation.router)
app.include_router(rooms.router)
app.include_router(auth.router)
app.include_router(report.router)


# It just for testing purposes
@app.get("/")
async def root():
    return {"message": "Hello World"}


def main():
    logger.info("App starting...")
    uvicorn.run("main:app", host="localhost", port=8080)

# /docs - /redoc for swagger
# All routes are available at /docs

if __name__ == '__main__':
    main()
