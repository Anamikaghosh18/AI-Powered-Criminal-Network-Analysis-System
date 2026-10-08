# Neo4j Current Schema

This document details the actual schema currently instantiated in the Neo4j Knowledge Graph.

## Node Labels and Properties

| Label | Properties | Unique Identifiers | Constraints/Indexes |
|-------|------------|--------------------|---------------------|
| `Crime` | `id`, `case_number`, `description`, `arrest`, `domestic`, `iucr`, `beat`, `year`, `source`, `source_record_id` | `id` (e.g. `crime:12345`) | `crime_id_unique` |
| `CrimeType` | `name` | `name` | `crimetype_name_unique` |
| `Location` | `id`, `latitude`, `longitude`, `block`, `location_description` | `id` (e.g. `loc:41.1:-87.2` or `block:...`) | `location_id_unique` |
| `District` | `id` | `id` | `district_id_unique` |
| `Ward` | `id` | `id` | `ward_id_unique` |
| `CommunityArea`| `id` | `id` | `communityarea_id_unique` |
| `Time` | `id`, `date`, `year` | `id` (e.g. `2025-06-20`) | `time_id_unique` |

## Relationship Types

| Source Node | Relationship | Target Node | Direction |
|-------------|--------------|-------------|-----------|
| `Crime` | `HAS_TYPE` | `CrimeType` | `Crime` -> `CrimeType` |
| `Crime` | `OCCURRED_AT`| `Location` | `Crime` -> `Location` |
| `Crime` | `IN_DISTRICT`| `District` | `Crime` -> `District` |
| `Crime` | `IN_WARD` | `Ward` | `Crime` -> `Ward` |
| `Crime` | `IN_COMMUNITY_AREA` | `CommunityArea` | `Crime` -> `CommunityArea` |
| `Crime` | `OCCURRED_ON`| `Time` | `Crime` -> `Time` |

## Notes
- Identifiers (`id`) across all nodes are string-based and deterministically derived.
- Constraints enforce uniqueness on `id` (or `name` for `CrimeType`) avoiding duplication.
- Nodes maintain provenance where applicable (e.g. `source`, `source_record_id`).
