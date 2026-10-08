from knowledge_graph.queries.query_runner import QueryRunner

class TemporalQueries(QueryRunner):
    def get_crimes_by_year(self):
        query = """
        MATCH (c:Crime)-[:OCCURRED_ON]->(t:Time)
        RETURN t.year AS year, count(c) AS crime_count
        ORDER BY year ASC
        """
        return self.run_read_query(query)

    def get_crime_type_by_year(self):
        query = """
        MATCH (t:Time)<-[:OCCURRED_ON]-(c:Crime)-[:HAS_TYPE]->(ct:CrimeType)
        RETURN t.year AS year, ct.name AS crime_type, count(c) AS crime_count
        ORDER BY year ASC, crime_count DESC
        """
        return self.run_read_query(query)

    def get_district_crimes_by_year(self):
        query = """
        MATCH (d:District)<-[:IN_DISTRICT]-(c:Crime)-[:OCCURRED_ON]->(t:Time)
        RETURN d.id AS district, t.year AS year, count(c) AS crime_count
        ORDER BY district, year ASC
        """
        return self.run_read_query(query)
