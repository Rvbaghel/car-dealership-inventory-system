from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from app.config import get_db
from app.entities.vehicle_entity import Vehicle, VehicleCreateRequest
from app.security.jwt_handler import SecurityUtils

router = APIRouter(prefix="/api/vehicles", tags=["Vehicle Controller Layer"])

@router.post("", status_code=status.HTTP_201_CREATED)
def create_vehicle(request: VehicleCreateRequest, db: Session = Depends(get_db), authorization: str = Header(None)):
    """Happy Path Entrypoint: Verifies structural token layout and saves a new vehicle."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Missing or invalid Authorization header structural format"
        )
    
    token = authorization.split(" ")[1]
    # Audits signature validity and identity tracking claims
    SecurityUtils.verify_access_token(token)

    db_vehicle = Vehicle(
        make=request.make,
        model=request.model,
        category=request.category,
        price=request.price,
        quantity=request.quantity
    )
    
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@router.get("", status_code=status.HTTP_200_OK)
def get_all_vehicles(db: Session = Depends(get_db), authorization: str = Header(None)):
    """Happy Path Entrypoint: Verifies structural token layout and fetches all vehicles."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Missing or invalid Authorization header structural format"
        )
    
    token = authorization.split(" ")[1]
    SecurityUtils.verify_access_token(token)

    # Fetch all items matching our database vehicle entity definition
    vehicles = db.query(Vehicle).all()
    return vehicles

