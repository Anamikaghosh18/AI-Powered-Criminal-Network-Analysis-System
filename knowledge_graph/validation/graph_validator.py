import logging
from neo4j import GraphDatabase
from knowledge_graph.config.settings import settings
from knowledge_graph.validation.validation_queries import ValidationQueries

logger = logging.getLogger(__name__)

class GraphValidator:
    def __init__(self, uri=None, user=None, password=None):
        self.uri = uri or settings.neo4j_uri
        self.user = user or settings.neo4j_username
        self.password = password or settings.neo4j_password
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        self.driver.close()

    def run_query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return [record.data() for record in result]

    def validate(self):
        report = []
        report.append("========================================")
        report.append("NEO4J GRAPH VALIDATION REPORT")
        report.append("========================================\n")

        # 1. Connectivity
        report.append("[1] DATABASE CONNECTIVITY")
        try:
            self.driver.verify_connectivity()
            report.append("Status: PASS\n")
        except Exception as e:
            report.append(f"Status: FAIL - {e}\n")
            return "\n".join(report)

        # 2. Node Counts
        report.append("[2] NODE COUNTS")
        nodes = self.run_query(ValidationQueries.NODES_BY_LABEL)
        for n in nodes:
            report.append(f"{n['label']}: {n['count']}")
        report.append("")

        # 3. Relationship Counts
        report.append("[3] RELATIONSHIP COUNTS")
        rels = self.run_query(ValidationQueries.RELATIONSHIPS_BY_TYPE)
        for r in rels:
            report.append(f"{r['relationshipType']}: {r['count']}")
        report.append("")

        # 4. Crime Data Quality
        report.append("[4] CRIME DATA QUALITY")
        missing_id = self.run_query(ValidationQueries.MISSING_ID)[0]['count']
        report.append(f"Missing ID: {missing_id}")
        
        crime_props = self.run_query(ValidationQueries.CRIME_MISSING_PROPERTIES)[0]
        total = crime_props['total'] or 1 # avoid div by zero
        report.append(f"Missing Case Number: {crime_props['missing_case']} ({(crime_props['missing_case']/total)*100:.2f}%)")
        report.append(f"Missing Year: {crime_props['missing_year']} ({(crime_props['missing_year']/total)*100:.2f}%)")
        report.append(f"Missing Arrest Flag: {crime_props['missing_arrest']} ({(crime_props['missing_arrest']/total)*100:.2f}%)\n")

        # 5. Relationship Integrity
        report.append("[5] RELATIONSHIP INTEGRITY")
        report.append(f"Crimes without type: {self.run_query(ValidationQueries.ORPHAN_CRIMES_TYPE)[0]['count']}")
        report.append(f"Crimes without location: {self.run_query(ValidationQueries.ORPHAN_CRIMES_LOCATION)[0]['count']}")
        report.append(f"Crimes without district: {self.run_query(ValidationQueries.ORPHAN_CRIMES_DISTRICT)[0]['count']}\n")

        # 6. Geographic Validation
        report.append("[6] GEOGRAPHIC VALIDATION")
        geo = self.run_query(ValidationQueries.GEO_VALIDATION)[0]
        report.append(f"Total Locations: {geo['total']}")
        report.append(f"Missing coordinates (block only): {geo['missing_coords']}")
        report.append(f"Invalid latitude: {geo['invalid_lat']}")
        report.append(f"Invalid longitude: {geo['invalid_lon']}\n")

        # 7. Temporal Validation
        report.append("[7] TEMPORAL VALIDATION")
        temp = self.run_query(ValidationQueries.TEMPORAL_VALIDATION)[0]
        report.append(f"Earliest date: {temp.get('earliest', 'N/A')}")
        report.append(f"Latest date: {temp.get('latest', 'N/A')}\n")

        report.append("========================================")
        
        # Determine Status
        status = "PASS"
        if missing_id > 0 or geo['invalid_lat'] > 0 or geo['invalid_lon'] > 0:
            status = "FAIL"
        elif crime_props['missing_case'] > 0:
            status = "WARNING"
            
        report.append("FINAL STATUS")
        report.append("========================================")
        report.append(status)
        report.append("========================================")

        return "\n".join(report)

if __name__ == "__main__":
    validator = GraphValidator()
    print(validator.validate())
    validator.close()
