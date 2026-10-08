import argparse
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
from etl.postgres_models import Base
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_postgres(database_url: str):
    logger.info(f"Connecting to PostgreSQL at {database_url}...")
    engine = create_engine(database_url)
    
    logger.info("Creating tables...")
    Base.metadata.create_all(engine)
    logger.info("Tables created successfully.")

if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--db-url", type=str, default=os.getenv("POSTGRES_URL", "postgresql://postgres:password@localhost:5433/chicagocrime"))
    args = parser.parse_args()
    
    setup_postgres(args.db_url)
