# Graph AI Foundation

This module contains the skeletal structure for the Graph AI capabilities of the AI-Based Crime Network Intelligence System. 

It is designed to cleanly integrate with Neo4j Graph Data Science (GDS) and NetworkX.

## Current State
This module is strictly an **infrastructure foundation**. It contains:
- Abstractions for graph projections in Neo4j GDS.
- Interface definitions for future algorithms (Centrality, Community Detection, Similarity, Link Prediction, Path Analysis).

**NOTE:** There is NO model training, NO fake data population, and NO execution of algorithms against actual crime data at this stage.

## Planned Algorithms
- **Centrality**: Degree, Betweenness, PageRank (to find key entities).
- **Community Detection**: Louvain, Leiden (to find criminal groups).
- **Similarity**: Node similarity (to find similar behaviors/events).
- **Link Prediction**: To infer hidden relationships between entities.
- **Path Analysis**: Shortest paths and multi-hop neighborhood queries.
