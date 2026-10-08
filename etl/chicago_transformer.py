import logging
import pandas as pd

logger = logging.getLogger(__name__)

class ChicagoDataTransformer:
    @staticmethod
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies necessary transformations to the raw dataframe before database insertion.
        """
        # Drop completely empty rows
        df = df.dropna(how='all')
        
        # Ensure correct boolean types for Arrest and Domestic
        if 'arrest' in df.columns:
            df['arrest'] = df['arrest'].astype(bool)
        if 'domestic' in df.columns:
            df['domestic'] = df['domestic'].astype(bool)
            
        # Standardize strings
        if 'primary_type' in df.columns:
            df['primary_type'] = df['primary_type'].str.strip().str.upper()
            
        return df
