import logging
from knowledge_graph.graph.connection import Neo4jConnection
from knowledge_graph.graph.constraints import create_constraints_and_indexes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Initializing Neo4j connection...")
    conn = Neo4jConnection()
    
    if conn.verify_connectivity():
        logger.info("Connection successful. Setting up constraints and indexes...")
        create_constraints_and_indexes(conn)
        logger.info("Setup complete.")
    else:
        logger.error("Failed to connect to Neo4j. Please check your configuration and ensure Neo4j is running.")
        
    conn.close()

if __name__ == "__main__":
    main()
