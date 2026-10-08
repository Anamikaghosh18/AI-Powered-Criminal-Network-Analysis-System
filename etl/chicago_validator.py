import logging

logger = logging.getLogger(__name__)

class ChicagoDataValidator:
    @staticmethod
    def validate_row(row: dict) -> bool:
        """
        Validate a single row of Chicago Crimes data.
        Returns True if valid, False otherwise.
        """
        # Essential fields must exist
        if not row.get('crime_id') or not row.get('case_number'):
            return False
            
        # Latitude and longitude must be in valid ranges if present
        if row.get('latitude') and (row['latitude'] < -90 or row['latitude'] > 90):
            return False
        if row.get('longitude') and (row['longitude'] < -180 or row['longitude'] > 180):
            return False
            
        return True
