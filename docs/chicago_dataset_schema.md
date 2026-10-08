# Chicago Crimes Dataset Schema

This document maps the raw CSV columns from the "Chicago Crimes – 2001 to Present" dataset to the Knowledge Graph representation.

| CSV Column           | Data Type | Meaning                               | Important? | PostgreSQL Mapping     | KG Mapping                               |
| -------------------- | --------- | ------------------------------------- | ---------- | ---------------------- | ---------------------------------------- |
| ID                   | integer   | Crime record identifier               | Yes        | `crime_id`             | `Crime.id` (`crime:{ID}`)                |
| Case Number          | string    | Police case identifier                | Yes        | `case_number`          | `Crime.case_number`                      |
| Date                 | datetime  | Crime date/time                       | Yes        | `date`                 | `Time` node & `Crime.date`               |
| Block                | string    | Partially redacted address            | Yes        | `block`                | `Location.block`                         |
| IUCR                 | string    | Illinois Uniform Crime Reporting code | No         | `iucr`                 | `Crime.iucr`                             |
| Primary Type         | string    | Main crime category                   | Yes        | `primary_type`         | `CrimeType` node                         |
| Description          | string    | Detailed crime description            | Yes        | `description`          | `Crime.description`                      |
| Location Description | string    | Location category                     | Yes        | `location_description` | `Location.location_description`          |
| Arrest               | boolean   | Arrest made                           | Yes        | `arrest`               | `Crime.arrest`                           |
| Domestic             | boolean   | Domestic incident flag                | Yes        | `domestic`             | `Crime.domestic`                         |
| Beat                 | integer   | Police beat                           | No         | `beat`                 | `Crime.beat`                             |
| District             | integer   | Police district                       | Yes        | `district`             | `District` node                          |
| Ward                 | integer   | Political ward                        | Yes        | `ward`                 | `Ward` node                              |
| Community Area       | integer   | Community area                        | Yes        | `community_area`       | `CommunityArea` node                     |
| FBI Code             | string    | FBI crime classification code         | No         | `fbi_code`             | `Crime.fbi_code`                         |
| X Coordinate         | float     | X Coordinate                          | No         | `x_coordinate`         | -                                        |
| Y Coordinate         | float     | Y Coordinate                          | No         | `y_coordinate`         | -                                        |
| Year                 | integer   | Year of occurrence                    | Yes        | `year`                 | `Time.year`                              |
| Updated On           | datetime  | Last updated timestamp                | No         | `updated_on`           | `Crime.updated_on`                       |
| Latitude             | float     | Latitude                              | Yes        | `latitude`             | `Location.latitude`                      |
| Longitude            | float     | Longitude                             | Yes        | `longitude`            | `Location.longitude`                     |
| Location             | string    | Point tuple (Lat, Lon)                | No         | -                      | -                                        |

## Notes
- No fake `Person` or offender nodes are inferred from this dataset. 
- Location nodes are constructed from Latitude/Longitude (or block if missing coordinates).
- Nodes to be created: `Crime`, `CrimeType`, `Location`, `District`, `Ward`, `CommunityArea`, `Time`.
- All nodes maintain source provenance referencing the original CSV row ID.
