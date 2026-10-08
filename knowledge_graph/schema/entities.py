from typing import Optional
from pydantic import BaseModel, Field

class BaseEntity(BaseModel):
    """Base class for all entities in the Knowledge Graph."""
    id: str = Field(..., description="Canonical ID for the entity")
    source: Optional[str] = Field(None, description="Source of the entity (e.g., nlp, cv, official_record)")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score")

class Person(BaseEntity):
    name: Optional[str] = None
    external_id: Optional[str] = None

class Crime(BaseEntity):
    crime_type: str
    description: Optional[str] = None
    timestamp: Optional[str] = None

class Location(BaseEntity):
    name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None

class Organization(BaseEntity):
    name: str
    organization_type: Optional[str] = None

class Vehicle(BaseEntity):
    vehicle_type: Optional[str] = None
    registration: Optional[str] = None

class Case(BaseEntity):
    case_number: Optional[str] = None
    created_at: Optional[str] = None

class Evidence(BaseEntity):
    type: str

class Event(BaseEntity):
    event_type: str
    timestamp: str
