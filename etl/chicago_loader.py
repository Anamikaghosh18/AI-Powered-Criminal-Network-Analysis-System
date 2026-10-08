import pandas as pd
from sqlalchemy import create_engine
import argparse
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data(csv_path: str, db_url: str, limit: int = None):
    logger.info(f"Loading data from {csv_path} (Limit: {limit})")
    
    # Define columns to read and map them to db column names
    col_mapping = {
        'ID': 'crime_id',
        'Case Number': 'case_number',
        'Date': 'date',
        'Block': 'block',
        'IUCR': 'iucr',
        'Primary Type': 'primary_type',
        'Description': 'description',
        'Location Description': 'location_description',
        'Arrest': 'arrest',
        'Domestic': 'domestic',
        'Beat': 'beat',
        'District': 'district',
        'Ward': 'ward',
        'Community Area': 'community_area',
        'FBI Code': 'fbi_code',
        'X Coordinate': 'x_coordinate',
        'Y Coordinate': 'y_coordinate',
        'Year': 'year',
        'Updated On': 'updated_on',
        'Latitude': 'latitude',
        'Longitude': 'longitude'
    }
    
    # Read chunk by chunk for memory efficiency
    chunksize = 10000
    engine = create_engine(db_url)
    
    nrows = limit if limit else None
    
    try:
        # We read the entire file if no limit, but use chunks
        if limit:
            df = pd.read_csv(csv_path, nrows=limit, usecols=col_mapping.keys())
            process_dataframe(df, col_mapping, engine)
        else:
            for chunk in pd.read_csv(csv_path, chunksize=chunksize, usecols=col_mapping.keys()):
                process_dataframe(chunk, col_mapping, engine)
                
        logger.info("Data loading complete.")
    except Exception as e:
        logger.error(f"Failed to load data: {e}")

def process_dataframe(df: pd.DataFrame, col_mapping: dict, engine):
    df = df.rename(columns=col_mapping)
    
    # Clean Data
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
    df['updated_on'] = pd.to_datetime(df['updated_on'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
    df['arrest'] = df['arrest'].astype(bool)
    df['domestic'] = df['domestic'].astype(bool)
    
    # Fill numeric NaNs where necessary for integer columns before inserting
    # District, Ward, Community Area, Beat can be float if missing values are present
    int_cols = ['beat', 'district', 'ward', 'community_area', 'year']
    for col in int_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(-1).astype(int)

    # Insert into PostgreSQL
    df.to_sql('chicago_crimes', engine, if_exists='append', index=False, method='multi', chunksize=1000)
    logger.info(f"Inserted {len(df)} rows.")

if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default="data/raw/chicago_crimes.csv")
    parser.add_argument("--db-url", type=str, default=os.getenv("POSTGRES_URL", "postgresql://postgres:password@localhost:5433/chicagocrime"))
    parser.add_argument("--limit", type=int, default=None, help="Limit number of rows to import")
    args = parser.parse_args()
    
    load_data(args.file, args.db_url, args.limit)
