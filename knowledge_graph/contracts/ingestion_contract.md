# NLP/CV Integration Contract

This contract defines exactly how the NLP and CV teams must format their outputs to be ingested into the Knowledge Graph. 

**IMPORTANT: The NLP and CV teams do not need to understand Neo4j or Graph DB internals. They simply output data matching this JSON contract.**

## Canonical Entity ID Strategy
All entities must use a stable canonical ID format. **Do not use names as primary identifiers.**
Format: `<type>:<unique_identifier>`
Examples:
- `person:12345`
- `crime:robbery-998`
- `vehicle:lp-XYZ123`

## Generic Input Format

The ingestion layer expects a JSON payload containing `entities` and `relationships`.

```json
{
  "entities": [
    {
      "id": "person:123",
      "type": "Person",
      "properties": {
        "name": "Example Person"
      },
      "confidence": 0.94,
      "source": "nlp"
    }
  ],
  "relationships": [
    {
      "source": "person:123",
      "type": "INVOLVED_IN",
      "target": "crime:456",
      "confidence": 0.89,
      "source": "nlp"
    }
  ]
}
```

## Rules
- **Entities**: 
  - `id` (required): Must follow the Canonical ID strategy.
  - `type` (required): Must be one of `Person`, `Crime`, `Location`, `Organization`, `Vehicle`, `Case`, `Evidence`, `Event`.
  - `properties`: Object containing fields specific to the entity type.
  - `confidence` (optional): Float between 0.0 and 1.0.
  - `source`: E.g., `nlp`, `cv`, `official_record`.
- **Relationships**:
  - `source` (required): Canonical ID of the source entity.
  - `target` (required): Canonical ID of the target entity.
  - `type` (required): Must be from the controlled vocabulary (e.g., `INVOLVED_IN`, `LOCATED_AT`, `RELATED_TO`).
  - `confidence` (optional): Float between 0.0 and 1.0.
  - `source`: E.g., `nlp`, `cv`.
  - `evidence_id` (optional): Canonical ID linking to the `Evidence` node that supports this extraction.
