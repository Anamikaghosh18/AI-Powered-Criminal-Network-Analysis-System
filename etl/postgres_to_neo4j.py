import argparse
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
import pandas as pd
from neo4j import GraphDatabase
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_neo4j_ingestion(db_url: str, neo4j_uri: str, neo4j_user: str, neo4j_password: str, limit: int = None):
    logger.info("Connecting to Postgres...")
    engine = create_engine(db_url)
    
    query = "SELECT * FROM chicago_crimes"
    if limit:
        query += f" LIMIT {limit}"
        
    df = pd.read_sql(query, engine)
    logger.info(f"Loaded {len(df)} records from Postgres.")
    
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    
    cypher_query = """
    UNWIND $batch AS row
    
    // 1. Crime Node
    MERGE (c:Crime {id: 'crime:' + toString(row.crime_id)})
    SET c.case_number = row.case_number,
        c.description = row.description,
        c.arrest = row.arrest,
        c.domestic = row.domestic,
        c.iucr = row.iucr,
        c.beat = row.beat,
        c.year = row.year,
        c.source = 'Chicago Crimes Dataset',
        c.source_record_id = toString(row.crime_id)
        
    // 2. Crime Type
    MERGE (t:CrimeType {name: row.primary_type})
    MERGE (c)-[:HAS_TYPE]->(t)
    
    // 3. Location
    WITH c, row, 
         CASE WHEN row.latitude IS NOT NULL THEN 'loc:' + toString(row.latitude) + ':' + toString(row.longitude)
              ELSE 'block:' + row.block END AS loc_id
    MERGE (l:Location {id: loc_id})
    ON CREATE SET l.latitude = row.latitude,
                  l.longitude = row.longitude,
                  l.block = row.block,
                  l.location_description = row.location_description
    MERGE (c)-[:OCCURRED_AT]->(l)
    
    // 4. District
    MERGE (d:District {id: toString(row.district)})
    MERGE (c)-[:IN_DISTRICT]->(d)
    
    // 5. Ward
    MERGE (w:Ward {id: toString(row.ward)})
    MERGE (c)-[:IN_WARD]->(w)
    
    // 6. Community Area
    MERGE (ca:CommunityArea {id: toString(row.community_area)})
    MERGE (c)-[:IN_COMMUNITY_AREA]->(ca)
    
    // 7. Time Node
    WITH c, row
    WHERE row.date IS NOT NULL
    WITH c, row, substring(toString(row.date), 0, 10) as date_str
    MERGE (t_node:Time {id: date_str})
    ON CREATE SET t_node.date = date_str,
                  t_node.year = row.year
    MERGE (c)-[:OCCURRED_ON]->(t_node)
    """
    
    # Process in batches
    batch_size = 1000
    records = df.to_dict('records')
    
    with driver.session() as session:
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            session.run(cypher_query, batch=batch)
            logger.info(f"Processed batch {i} to {i+len(batch)}")
            
    driver.close()
    logger.info("Neo4j ingestion complete.")

if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--db-url", type=str, default=os.getenv("POSTGRES_URL", "postgresql://postgres:password@localhost:5433/chicagocrime"))
    parser.add_argument("--neo4j-uri", type=str, default=os.getenv("NEO4J_URI", "bolt://localhost:7687"))
    parser.add_argument("--neo4j-user", type=str, default=os.getenv("NEO4J_USERNAME", "neo4j"))
    parser.add_argument("--neo4j-password", type=str, default=os.getenv("NEO4J_PASSWORD", "password"))
    parser.add_argument("--limit", type=int, default=None, help="Limit number of rows to import")
    args = parser.parse_args()
    
    run_neo4j_ingestion(args.db_url, args.neo4j_uri, args.neo4j_user, args.neo4j_password, args.limit)
