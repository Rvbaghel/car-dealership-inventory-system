from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from app.config import get_db
from app.entities.vehicle_entity import Vehicle, VehicleCreateRequest
from app.security.jwt_handler import SecurityUtils
from typing import Optional
from pydantic import BaseModel

router = APIRouter(prefix="/api/vehicles", tags=["Vehicle Controller Layer"])

class VehicleRestockRequest(BaseModel):
    quantity: int

@router.post("", status_code=status.HTTP_201_CREATED)
def create_vehicle(
    request: VehicleCreateRequest, 
    db: Session = Depends(get_db), 
    authorization: Optional[str] = Header(None, alias="Authorization")
):
    """Happy Path Entrypoint: Securely verifies administrative permissions and adds a new vehicle."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Missing or invalid Authorization header structural format"
        )
    
    token = authorization.split(" ")[1]
    # Decode the payload claims dictionary
    payload = SecurityUtils.verify_access_token(token)
    
    # Secure validation layer: Force ADMIN authorization check
    if payload.get("role") != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privileges required to add inventory items"
        )

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
def get_all_vehicles(
    db: Session = Depends(get_db), 
    authorization: Optional[str] = Header(None, alias="Authorization")  # Fixed tracking alias mapping
):
    """Happy Path Entrypoint: Verifies structural token layout and fetches all vehicles."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Missing or invalid Authorization header structural format"
        )
    
    token = authorization.split(" ")[1]
    SecurityUtils.verify_access_token(token)

    vehicles = db.query(Vehicle).all()
    return vehicles

@router.get("/search", status_code=status.HTTP_200_OK)
def search_vehicles(
    make: Optional[str] = None,
    model: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None, alias="Authorization")  # Fixed tracking alias mapping
):
    """Happy Path Entrypoint: Dynamic search filtering engine for vehicle inventory."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Missing or invalid Authorization header structural format"
        )
    
    token = authorization.split(" ")[1]
    SecurityUtils.verify_access_token(token)

    query = db.query(Vehicle)
    if make:
        query = query.filter(Vehicle.make.ilike(f"%{make}%"))
    if model:
        query = query.filter(Vehicle.model.ilike(f"%{model}%"))
    if category:
        query = query.filter(Vehicle.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(Vehicle.price >= min_price)
    if max_price is not None:
        query = query.filter(Vehicle.price <= max_price)

    return query.all()

@router.put("/{vehicle_id}", status_code=status.HTTP_200_OK)
def update_vehicle(
    vehicle_id: int,
    request: VehicleCreateRequest,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None, alias="Authorization")
):
    """Happy Path Entrypoint: Updates an existing vehicle resource's tracking details (ADMIN Only)."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Missing or invalid Authorization header structural format"
        )
    
    token = authorization.split(" ")[1]
    # Decode payload to parse role permissions securely
    payload = SecurityUtils.verify_access_token(token)
    
    # Secure role verification block
    if payload.get("role") != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privileges required to update inventory items"
        )

    # Search for the vehicle in the database
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    # Mutate the resource state attributes
    db_vehicle.make = request.make
    db_vehicle.model = request.model
    db_vehicle.category = request.category
    db_vehicle.price = request.price
    db_vehicle.quantity = request.quantity

    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@router.delete("/{vehicle_id}", status_code=status.HTTP_200_OK)
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None, alias="Authorization")  # Fixed tracking alias mapping
):
    """Happy Path Entrypoint: Verifies administrative claims and purges a vehicle."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Missing or invalid Authorization header structural format"
        )
    
    token = authorization.split(" ")[1]
    payload = SecurityUtils.verify_access_token(token)
    
    if payload.get("role") != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privileges required to perform this action"
        )

    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    db.delete(db_vehicle)
    db.commit()
    #return message
    return {"message": "Vehicle deleted successfully"}

@router.post("/{vehicle_id}/restock", status_code=status.HTTP_200_OK)
def restock_vehicle(
    vehicle_id: int,
    request: VehicleRestockRequest,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None, alias="Authorization")
):
    """Happy Path Entrypoint: Authenticates ADMIN role and increments vehicle inventory stock."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Missing or invalid Authorization header structural format"
        )
    
    token = authorization.split(" ")[1]
    payload = SecurityUtils.verify_access_token(token)
    
    # Secure role verification block
    if payload.get("role") != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privileges required to restock inventory"
        )

    # Search for the vehicle in the database
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

    # Increment the quantity
    db_vehicle.quantity += request.quantity

    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle