from neo4j import GraphDatabase
import logging
from knowledge_graph.config.settings import settings

logger = logging.getLogger(__name__)

class Neo4jConnection:
    def __init__(self, uri=None, user=None, password=None, database=None):
        self.uri = uri or settings.neo4j_uri
        self.user = user or settings.neo4j_username
        self.password = password or settings.neo4j_password
        self.database = database or settings.neo4j_database
        self.driver = None
        
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        except Exception as e:
            logger.error(f"Failed to create Neo4j driver: {e}")

    def close(self):
        if self.driver:
            self.driver.close()

    def verify_connectivity(self):
        try:
            self.driver.verify_connectivity()
            return True
        except Exception as e:
            logger.error(f"Connectivity check failed: {e}")
            return False

    def get_session(self, **kwargs):
        return self.driver.session(database=self.database, **kwargs)
