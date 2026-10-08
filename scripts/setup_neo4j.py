import argparse
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_neo4j_constraints(uri, user, password):
    logger.info("Setting up Neo4j constraints for Chicago Crimes...")
    
    queries = [
        "CREATE CONSTRAINT crime_id_unique IF NOT EXISTS FOR (c:Crime) REQUIRE c.id IS UNIQUE",
        "CREATE CONSTRAINT crimetype_name_unique IF NOT EXISTS FOR (t:CrimeType) REQUIRE t.name IS UNIQUE",
        "CREATE CONSTRAINT location_id_unique IF NOT EXISTS FOR (l:Location) REQUIRE l.id IS UNIQUE",
        "CREATE CONSTRAINT district_id_unique IF NOT EXISTS FOR (d:District) REQUIRE d.id IS UNIQUE",
        "CREATE CONSTRAINT ward_id_unique IF NOT EXISTS FOR (w:Ward) REQUIRE w.id IS UNIQUE",
        "CREATE CONSTRAINT communityarea_id_unique IF NOT EXISTS FOR (ca:CommunityArea) REQUIRE ca.id IS UNIQUE",
        "CREATE CONSTRAINT time_id_unique IF NOT EXISTS FOR (t:Time) REQUIRE t.id IS UNIQUE"
    ]
    
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    with driver.session() as session:
        for query in queries:
            try:
                session.run(query)
                logger.info(f"Executed: {query}")
            except Exception as e:
                logger.error(f"Failed to execute '{query}': {e}")
                
    driver.close()

if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--uri", type=str, default=os.getenv("NEO4J_URI", "bolt://localhost:7687"))
    parser.add_argument("--user", type=str, default=os.getenv("NEO4J_USERNAME", "neo4j"))
    parser.add_argument("--password", type=str, default=os.getenv("NEO4J_PASSWORD", "password"))
    args = parser.parse_args()
    
    setup_neo4j_constraints(args.uri, args.user, args.password)
