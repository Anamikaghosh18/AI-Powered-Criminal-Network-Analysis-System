from neo4j import GraphDatabase
from knowledge_graph.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class QueryRunner:
    """Base class for executing Neo4j queries."""
    
    def __init__(self, uri=None, user=None, password=None):
        self.uri = uri or settings.neo4j_uri
        self.user = user or settings.neo4j_username
        self.password = password or settings.neo4j_password
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        self.driver.close()

    def run_read_query(self, query, **parameters):
        """Executes a read query and returns a list of dictionaries."""
        with self.driver.session() as session:
            try:
                result = session.run(query, **parameters)
                return [record.data() for record in result]
            except Exception as e:
                logger.error(f"Failed to execute query: {e}")
                return []
