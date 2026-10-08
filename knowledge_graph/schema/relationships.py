from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class Relationship(BaseModel):
    """Base class for all relationships in the Knowledge Graph."""
    source_id: str = Field(..., description="Canonical ID of the source entity")
    target_id: str = Field(..., description="Canonical ID of the target entity")
    type: str = Field(..., description="The type of the relationship (e.g., INVOLVED_IN)")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score")
    source: Optional[str] = Field(None, description="Source of the relationship")
    timestamp: Optional[str] = Field(None, description="Timestamp of when the relationship occurred or was recorded")
    evidence_id: Optional[str] = Field(None, description="Canonical ID of the evidence supporting this relationship")
    properties: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata properties")

VALID_RELATIONSHIP_TYPES = {
    "INVOLVED_IN",
    "ASSOCIATED_WITH",
    "MEMBER_OF",
    "LOCATED_AT",
    "OCCURRED_AT",
    "RELATED_TO",
    "PART_OF_CASE",
    "CONNECTED_TO",
    "USED",
    "OBSERVED_AT",
    "MENTIONED_IN",
    "DERIVED_FROM"
}
