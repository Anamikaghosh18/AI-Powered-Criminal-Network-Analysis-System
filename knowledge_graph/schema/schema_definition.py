from enum import Enum

class NodeType(str, Enum):
    PERSON = "Person"
    CRIME = "Crime"
    LOCATION = "Location"
    ORGANIZATION = "Organization"
    VEHICLE = "Vehicle"
    CASE = "Case"
    EVIDENCE = "Evidence"
    EVENT = "Event"

class RelationshipType(str, Enum):
    INVOLVED_IN = "INVOLVED_IN"
    ASSOCIATED_WITH = "ASSOCIATED_WITH"
    MEMBER_OF = "MEMBER_OF"
    LOCATED_AT = "LOCATED_AT"
    OCCURRED_AT = "OCCURRED_AT"
    RELATED_TO = "RELATED_TO"
    PART_OF_CASE = "PART_OF_CASE"
    CONNECTED_TO = "CONNECTED_TO"
    USED = "USED"
    OBSERVED_AT = "OBSERVED_AT"
    MENTIONED_IN = "MENTIONED_IN"
    DERIVED_FROM = "DERIVED_FROM"
