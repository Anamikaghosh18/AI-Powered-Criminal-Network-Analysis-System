from knowledge_graph.queries.query_runner import QueryRunner

class CrimeQueries(QueryRunner):
    def get_total_crimes(self):
        query = "MATCH (c:Crime) RETURN count(c) AS total_crimes"
        result = self.run_read_query(query)
        return result[0]['total_crimes'] if result else 0

    def get_top_crime_types(self, limit: int = 10):
        query = """
        MATCH (c:Crime)-[:HAS_TYPE]->(t:CrimeType)
        RETURN t.name AS crime_type, count(c) AS count
        ORDER BY count DESC
        LIMIT $limit
        """
        return self.run_read_query(query, limit=limit)

    def get_arrest_statistics(self):
        query = """
        MATCH (c:Crime)-[:HAS_TYPE]->(t:CrimeType)
        WITH t.name AS crime_type, count(c) AS total_crimes, 
             sum(CASE WHEN c.arrest = true THEN 1 ELSE 0 END) AS arrests
        RETURN crime_type, total_crimes, arrests, 
               CASE WHEN total_crimes > 0 THEN toFloat(arrests)/total_crimes ELSE 0 END AS arrest_rate
        ORDER BY total_crimes DESC
        """
        return self.run_read_query(query)

    def get_domestic_vs_non_domestic(self):
        query = """
        MATCH (c:Crime)
        RETURN c.domestic AS domestic, count(c) AS crime_count
        ORDER BY crime_count DESC
        """
        return self.run_read_query(query)
