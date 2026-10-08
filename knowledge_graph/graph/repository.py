from typing import Dict, Any, List, Optional
from knowledge_graph.graph.connection import Neo4jConnection
from knowledge_graph.schema.entities import BaseEntity
from knowledge_graph.schema.relationships import Relationship
import logging

logger = logging.getLogger(__name__)

class GraphRepository:
    def __init__(self, connection: Neo4jConnection):
        self.conn = connection

    def create_or_merge_entity(self, label: str, entity: BaseEntity) -> Dict[str, Any]:
        """Merges an entity into the graph based on its ID."""
        query = f"""
        MERGE (n:{label} {{id: $properties.id}})
        SET n += $properties
        RETURN n
        """
        properties = entity.model_dump(exclude_none=True)
        with self.conn.get_session() as session:
            result = session.run(query, properties=properties)
            record = result.single()
            return dict(record["n"]) if record else {}

    def create_or_merge_relationship(self, source_label: str, target_label: str, relationship: Relationship) -> Dict[str, Any]:
        """Merges a relationship between two entities."""
        query = f"""
        MATCH (s:{source_label} {{id: $source_id}})
        MATCH (t:{target_label} {{id: $target_id}})
        MERGE (s)-[r:{relationship.type}]->(t)
        SET r += $properties, r.confidence = $confidence, r.source = $source
        RETURN r
        """
        props = relationship.properties or {}
        with self.conn.get_session() as session:
            result = session.run(
                query, 
                source_id=relationship.source_id,
                target_id=relationship.target_id,
                properties=props,
                confidence=relationship.confidence,
                source=relationship.source
            )
            record = result.single()
            return dict(record["r"]) if record else {}

    def get_entity_by_id(self, label: str, entity_id: str) -> Optional[Dict[str, Any]]:
        query = f"MATCH (n:{label} {{id: $id}}) RETURN n"
        with self.conn.get_session() as session:
            result = session.run(query, id=entity_id)
            record = result.single()
            return dict(record["n"]) if record else None
