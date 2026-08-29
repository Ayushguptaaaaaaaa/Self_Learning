from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
import math
from math import radians, sin, cos, sqrt, atan2


app = FastAPI()


locations_storage = {}


# Pydantic Models

class LocationRequest(BaseModel):
    name: str
    category: str
    lat: float
    lon: float


class LocationResponse(BaseModel):
    id: str
    name: str
    category: str
    lat: float
    lon: float


class NearbyLocationResponse(LocationResponse):
    distance: float


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth.
    Returns distance in kilometers.
    """
    R = 6371  # Earth's radius in km

    # Convert to radians
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    # Haversine formula
    a = sin(dlat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    distance = R * c
    return distance

@app.post("/locations", response_model=LocationResponse, status_code=201)
async def create_location(request: LocationRequest):
    """
    Register a new location.
    """
    # Generate unique location ID
    location_id = str(uuid.uuid4())
    
    # Create location entry
    location_data = {
        "id": location_id,
        "name": request.name,
        "category": request.category,
        "lat": request.lat,
        "lon": request.lon
    }
    
    # Store in locations_storage
    locations_storage[location_id] = location_data
    
    # Return the created location
    return LocationResponse(**location_data)


@app.get("/locations/{id}", response_model=LocationResponse)
async def get_location(id: str):
    """
    Get details of a specific location by ID.
    """
    # Check if location exists
    if id not in locations_storage:
        raise HTTPException(status_code=404, detail="Location not found")
    
    # Return the location data
    return LocationResponse(**locations_storage[id])


@app.get("/locations", response_model=list[LocationResponse])
async def list_locations(category: Optional[str] = None):
    """
    List all locations with optional category filter.
    """
    # If category filter is provided
    if category:
        filtered_locations = [
            LocationResponse(**location) 
            for location in locations_storage.values() 
            if location["category"] == category
        ]
        return filtered_locations
    
    # Return all locations if no filter
    return [LocationResponse(**location) for location in locations_storage.values()]

@app.get("/nearby", response_model=list[NearbyLocationResponse])
async def find_nearby(lat: float, lon: float, radius: float, category: Optional[str] = None):
    """
    Find all locations within a specified radius from a given coordinate.
    """
    results = []
    
    # Loop through all locations
    for location in locations_storage.values():
        # Calculate distance from search point to location
        distance = haversine_distance(lat, lon, location["lat"], location["lon"])
        
        # Check if within radius
        if distance <= radius:
            # Check category filter if provided
            if category is None or location["category"] == category:
                # Add location with distance to results
                results.append({**location, "distance": distance})
    
    # Sort results by distance (closest first)
    results.sort(key=lambda x: x["distance"])
    
    # Return sorted nearby locations
    return [NearbyLocationResponse(**loc) for loc in results]

@app.delete("/locations/{id}")
async def delete_location(id: str):
    """
    Delete a location by ID.
    """
    # Check if location exists
    if id not in locations_storage:
        raise HTTPException(status_code=404, detail="Location not found")
    
    # Delete the location
    del locations_storage[id]
    
    # Return success message
    return {"message": "Location deleted successfully"} 