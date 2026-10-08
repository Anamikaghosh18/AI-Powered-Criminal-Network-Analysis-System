import logging
from knowledge_graph.graph.connection import Neo4jConnection
from knowledge_graph.schema.schema_definition import NodeType

logger = logging.getLogger(__name__)

def create_constraints_and_indexes(conn: Neo4jConnection):
    """Creates necessary constraints and indexes in the Neo4j database."""
    queries = []
    
    # Unique ID constraints for all major node types
    for node_type in NodeType:
        queries.append(f"CREATE CONSTRAINT unique_{node_type.value.lower()}_id IF NOT EXISTS FOR (n:{node_type.value}) REQUIRE n.id IS UNIQUE")
    
    with conn.get_session() as session:
        for query in queries:
            try:
                session.run(query)
                logger.info(f"Executed: {query}")
            except Exception as e:
                logger.error(f"Failed to execute constraint query '{query}': {e}")
