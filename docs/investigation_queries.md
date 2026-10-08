# Investigation Queries

This document outlines the reusable Cypher queries available in the Python Query Interface.

## Crime Queries (`CrimeQueries`)

### Total Crimes
**Question**: How many crimes are in the graph?
**Graph Path**: `(c:Crime)`
**Output**: `total_crimes`
**Use Case**: Get the total dataset volume.

### Top Crime Types
**Question**: What are the most frequent crime categories?
**Graph Path**: `(Crime)-[:HAS_TYPE]->(CrimeType)`
**Inputs**: `limit`
**Output**: `crime_type`, `count`
**Use Case**: Identify the most common crime categories.

### Arrest Statistics
**Question**: Which crime types result in the most arrests?
**Graph Path**: `(Crime)-[:HAS_TYPE]->(CrimeType)`
**Output**: `crime_type`, `total_crimes`, `arrests`, `arrest_rate`
**Use Case**: Analyze law enforcement success rates per crime type.

### Domestic vs Non-Domestic
**Question**: How many crimes are domestic incidents?
**Graph Path**: `(Crime)`
**Output**: `domestic`, `crime_count`
**Use Case**: Measure the ratio of domestic incidents.

## Geographic Queries (`GeographicQueries`)

### Crimes by District
**Question**: How are crimes distributed across police districts?
**Graph Path**: `(Crime)-[:IN_DISTRICT]->(District)`
**Inputs**: Optional `district_id`
**Output**: `district`, `crime_count`
**Use Case**: Resource allocation based on district crime density.

### Crime Types by District
**Question**: What types of crime are most common in each district?
**Graph Path**: `(District)<-[:IN_DISTRICT]-(Crime)-[:HAS_TYPE]->(CrimeType)`
**Inputs**: Optional `district_id`
**Output**: `district`, `crime_type`, `crime_count`
**Use Case**: Understand local district crime patterns.

### Top Crime Locations
**Question**: Which specific blocks or coordinate points have the most crime?
**Graph Path**: `(Crime)-[:OCCURRED_AT]->(Location)`
**Inputs**: `limit`
**Output**: `location`, `crime_count`
**Use Case**: Identify crime hotspots.

### Location Crime Profile
**Question**: What is the distribution of crimes at a specific location?
**Graph Path**: `(Location)<-[:OCCURRED_AT]-(Crime)-[:HAS_TYPE]->(CrimeType)`
**Inputs**: `location_id`
**Output**: `location`, `crime_type`, `count`
**Use Case**: Deep dive into a specific hotspot's activities.

## Temporal Queries (`TemporalQueries`)

### Crimes by Year
**Question**: What is the annual trend of total crimes?
**Graph Path**: `(Crime)-[:OCCURRED_ON]->(Time)`
**Output**: `year`, `crime_count`
**Use Case**: Overall temporal trend analysis.

### Crime Type by Year
**Question**: How have specific crime categories trended over time?
**Graph Path**: `(Time)<-[:OCCURRED_ON]-(Crime)-[:HAS_TYPE]->(CrimeType)`
**Output**: `year`, `crime_type`, `crime_count`
**Use Case**: Track the rise or fall of specific crime types.

### District Crimes by Year
**Question**: How has the crime volume in each district changed over time?
**Graph Path**: `(District)<-[:IN_DISTRICT]-(Crime)-[:OCCURRED_ON]->(Time)`
**Output**: `district`, `year`, `crime_count`
**Use Case**: Track district safety improvements or degradation.
