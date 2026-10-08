import argparse
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_graph(uri, user, password):
    logger.info("Validating Chicago Crimes Knowledge Graph...")
    
    queries = {
        "Total Crimes": "MATCH (c:Crime) RETURN count(c) as result",
        "Total Crime Types": "MATCH (t:CrimeType) RETURN count(t) as result",
        "Total Locations": "MATCH (l:Location) RETURN count(l) as result",
        "Crimes by Type (Top 5)": """
            MATCH (c:Crime)-[:HAS_TYPE]->(t:CrimeType)
            RETURN t.name as label, count(c) as result
            ORDER BY result DESC LIMIT 5
        """,
        "Crimes by District (Top 5)": """
            MATCH (c:Crime)-[:IN_DISTRICT]->(d:District)
            RETURN d.id as label, count(c) as result
            ORDER BY result DESC LIMIT 5
        """
    }
    
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    with driver.session() as session:
        for name, query in queries.items():
            try:
                result = session.run(query)
                records = list(result)
                
                print(f"\n--- {name} ---")
                if len(records) == 1 and 'label' not in records[0]:
                    print(f"Count: {records[0]['result']}")
                else:
                    for record in records:
                        print(f"{record['label']}: {record['result']}")
                        
            except Exception as e:
                logger.error(f"Failed to execute '{name}': {e}")
                
    driver.close()
    logger.info("\nValidation complete.")

if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--uri", type=str, default=os.getenv("NEO4J_URI", "bolt://localhost:7687"))
    parser.add_argument("--user", type=str, default=os.getenv("NEO4J_USERNAME", "neo4j"))
    parser.add_argument("--password", type=str, default=os.getenv("NEO4J_PASSWORD", "password"))
    args = parser.parse_args()
    
    validate_graph(args.uri, args.user, args.password)
