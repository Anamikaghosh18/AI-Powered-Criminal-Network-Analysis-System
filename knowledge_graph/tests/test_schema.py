import pytest
from pydantic import ValidationError
from knowledge_graph.schema.entities import Person, Crime
from knowledge_graph.schema.relationships import Relationship

def test_valid_person_entity():
    person = Person(id="person:123", name="John Doe", confidence=0.9, source="nlp")
    assert person.id == "person:123"
    assert person.name == "John Doe"

def test_invalid_person_confidence():
    with pytest.raises(ValidationError):
        Person(id="person:123", confidence=1.5) 

def test_valid_relationship():
    rel = Relationship(
        source_id="person:123",
        target_id="crime:456",
        type="INVOLVED_IN",
        confidence=0.85
    )
    assert rel.type == "INVOLVED_IN"

def test_missing_relationship_fields():
    with pytest.raises(ValidationError):
        Relationship(source_id="person:123", type="INVOLVED_IN") 
