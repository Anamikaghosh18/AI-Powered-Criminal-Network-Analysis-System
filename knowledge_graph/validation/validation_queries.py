class ValidationQueries:
    TOTAL_NODES = "MATCH (n) RETURN count(n) AS total_nodes"
    
    NODES_BY_LABEL = """
    CALL db.labels() YIELD label
    MATCH (n) WHERE label IN labels(n)
    RETURN label, count(n) AS count
    ORDER BY count DESC
    """
    
    RELATIONSHIPS_BY_TYPE = """
    CALL db.relationshipTypes() YIELD relationshipType
    MATCH ()-[r]->() WHERE type(r) = relationshipType
    RETURN relationshipType, count(r) AS count
    ORDER BY count DESC
    """
    
    # Crime node validation
    MISSING_ID = "MATCH (c:Crime) WHERE c.id IS NULL RETURN count(c) AS count"
    
    CRIME_MISSING_PROPERTIES = """
    MATCH (c:Crime)
    WITH count(c) as total,
         sum(CASE WHEN c.case_number IS NULL THEN 1 ELSE 0 END) as missing_case,
         sum(CASE WHEN c.year IS NULL THEN 1 ELSE 0 END) as missing_year,
         sum(CASE WHEN c.arrest IS NULL THEN 1 ELSE 0 END) as missing_arrest
    RETURN total, missing_case, missing_year, missing_arrest
    """
    
    # Relationship integrity
    ORPHAN_CRIMES_TYPE = "MATCH (c:Crime) WHERE NOT (c)-[:HAS_TYPE]->() RETURN count(c) AS count"
    ORPHAN_CRIMES_LOCATION = "MATCH (c:Crime) WHERE NOT (c)-[:OCCURRED_AT]->() RETURN count(c) AS count"
    ORPHAN_CRIMES_DISTRICT = "MATCH (c:Crime) WHERE NOT (c)-[:IN_DISTRICT]->() RETURN count(c) AS count"
    
    # Geographic Validation
    GEO_VALIDATION = """
    MATCH (l:Location)
    WITH count(l) as total,
         sum(CASE WHEN l.latitude IS NULL OR l.longitude IS NULL THEN 1 ELSE 0 END) as missing_coords,
         sum(CASE WHEN l.latitude < -90 OR l.latitude > 90 THEN 1 ELSE 0 END) as invalid_lat,
         sum(CASE WHEN l.longitude < -180 OR l.longitude > 180 THEN 1 ELSE 0 END) as invalid_lon
    RETURN total, missing_coords, invalid_lat, invalid_lon
    """
    
    # Temporal Validation
    TEMPORAL_VALIDATION = """
    MATCH (t:Time)
    RETURN min(t.date) as earliest, max(t.date) as latest
    """
