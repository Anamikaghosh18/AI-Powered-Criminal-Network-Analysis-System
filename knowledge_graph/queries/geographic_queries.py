from knowledge_graph.queries.query_runner import QueryRunner

class GeographicQueries(QueryRunner):
    def get_crimes_by_district(self, district_id: str = None):
        if district_id:
            query = """
            MATCH (c:Crime)-[:IN_DISTRICT]->(d:District {id: $district_id})
            RETURN count(c) AS crime_count
            """
            result = self.run_read_query(query, district_id=str(district_id))
            return result[0]['crime_count'] if result else 0
        else:
            query = """
            MATCH (c:Crime)-[:IN_DISTRICT]->(d:District)
            RETURN d.id AS district, count(c) AS crime_count
            ORDER BY crime_count DESC
            """
            return self.run_read_query(query)

    def get_crime_types_by_district(self, district_id: str = None):
        query = """
        MATCH (c:Crime)-[:IN_DISTRICT]->(d:District)
        MATCH (c)-[:HAS_TYPE]->(t:CrimeType)
        """
        if district_id:
            query += "WHERE d.id = $district_id\n"
            
        query += """
        RETURN d.id AS district, t.name AS crime_type, count(c) AS crime_count
        ORDER BY district, crime_count DESC
        """
        return self.run_read_query(query, district_id=str(district_id) if district_id else None)

    def get_top_crime_locations(self, limit: int = 10):
        query = """
        MATCH (c:Crime)-[:OCCURRED_AT]->(l:Location)
        RETURN l.id AS location, count(c) AS crime_count
        ORDER BY crime_count DESC
        LIMIT $limit
        """
        return self.run_read_query(query, limit=limit)

    def get_crimes_by_community_area(self, area_id: str):
        query = """
        MATCH (c:Crime)-[:IN_COMMUNITY_AREA]->(ca:CommunityArea {id: $area_id})
        RETURN count(c) AS crime_count
        """
        result = self.run_read_query(query, area_id=str(area_id))
        return result[0]['crime_count'] if result else 0

    def get_location_crime_profile(self, location_id: str):
        query = """
        MATCH (l:Location {id: $location_id})<-[:OCCURRED_AT]-(c:Crime)-[:HAS_TYPE]->(t:CrimeType)
        RETURN l.id AS location, t.name AS crime_type, count(c) AS count
        ORDER BY count DESC
        """
        return self.run_read_query(query, location_id=location_id)
