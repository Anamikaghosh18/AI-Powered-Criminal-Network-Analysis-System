# Graph Projections for Chicago Crimes

This document explains the graph projections that can be derived from the base bipartite graph structure of the Chicago Crimes dataset.

## 1. Crime-Crime Similarity (Shared Location)
**Source Network**: `(Crime)-[:OCCURRED_AT]->(Location)<-[:OCCURRED_AT]-(Crime)`
**Projected Network**: `(Crime)-[:SHARED_LOCATION]->(Crime)`
**Purpose**: Identifies crimes that occur at the exact same coordinates or block. This can highlight recurring hotspots or organized activity concentrated at specific addresses.

## 2. Location-Location Similarity (Crime Profile)
**Source Network**: `(Location)<-[:OCCURRED_AT]-(Crime)-[:HAS_TYPE]->(CrimeType)<-[:HAS_TYPE]-(Crime)-[:OCCURRED_AT]->(Location)`
**Projected Network**: `(Location)-[:SIMILAR_CRIME_PROFILE]->(Location)`
**Purpose**: Connects locations that suffer from similar types of crimes. Useful for node similarity algorithms (e.g., Jaccard Similarity on CrimeTypes) to group geographic areas with identical security challenges.

## 3. District Crime Flows
**Projected Network**: `(District)-[:SIMILAR_DEMOGRAPHICS]->(District)` (Future extension)
**Purpose**: Comparing districts based on their aggregate crime distribution to detect macroscopic patterns in urban crime behavior.

**Note**: All projected relationships must have a clear analytical purpose. We do not project every possible combination.
