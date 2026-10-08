from unittest.mock import patch
from knowledge_graph.graph.connection import Neo4jConnection

@patch("knowledge_graph.graph.connection.GraphDatabase.driver")
def test_connection_initialization(mock_driver):
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="test", password="password")
    mock_driver.assert_called_once_with("bolt://localhost:7687", auth=("test", "password"))
    conn.close()
