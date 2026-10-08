import logging
from typing import List, Dict, Any
from knowledge_graph.graph.connection import Neo4jConnection

logger = logging.getLogger(__name__)

class GraphProjectionManager:
    """Manages Neo4j Graph Data Science (GDS) projections."""
    def __init__(self, connection: Neo4jConnection):
        self.conn = connection

    def create_projection(self, projection_name: str, node_labels: List[str], relationship_types: List[str]) -> Dict[str, Any]:
        """Creates a named graph projection for GDS algorithms."""
        query = """
        CALL gds.graph.project(
            $graph_name,
            $node_labels,
            $relationship_types
        ) YIELD graphName, nodeCount, relationshipCount
        """
        with self.conn.get_session() as session:
            try:
                result = session.run(query, graph_name=projection_name, node_labels=node_labels, relationship_types=relationship_types)
                record = result.single()
                return dict(record) if record else {}
            except Exception as e:
                logger.error(f"Failed to create projection {projection_name}: {e}")
                return {}

    def drop_projection(self, projection_name: str) -> bool:
        """Drops a named graph projection."""
        query = "CALL gds.graph.drop($graph_name) YIELD graphName"
        with self.conn.get_session() as session:
            try:
                session.run(query, graph_name=projection_name)
                return True
            except Exception as e:
                logger.error(f"Failed to drop projection {projection_name}: {e}")
                return False
