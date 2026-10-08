from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, Double, Integer, MetaData
from sqlalchemy.orm import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)

class CrimeRecord(Base):
    __tablename__ = 'chicago_crimes'
    
    crime_id = Column(BigInteger, primary_key=True)
    case_number = Column(String, index=True)
    date = Column(DateTime, index=True)
    block = Column(String)
    iucr = Column(String)
    primary_type = Column(String, index=True)
    description = Column(String)
    location_description = Column(String)
    arrest = Column(Boolean)
    domestic = Column(Boolean)
    beat = Column(Integer)
    district = Column(Integer, index=True)
    ward = Column(Integer)
    community_area = Column(Integer, index=True)
    fbi_code = Column(String)
    x_coordinate = Column(Double)
    y_coordinate = Column(Double)
    year = Column(Integer, index=True)
    updated_on = Column(DateTime)
    latitude = Column(Double, index=True)
    longitude = Column(Double, index=True)
