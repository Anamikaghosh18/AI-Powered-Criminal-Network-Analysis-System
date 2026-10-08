import pytest
from unittest.mock import patch, MagicMock
from knowledge_graph.queries.crime_queries import CrimeQueries
from knowledge_graph.queries.geographic_queries import GeographicQueries

@patch("knowledge_graph.queries.query_runner.GraphDatabase.driver")
def test_crime_queries(mock_driver_class):
    mock_driver = MagicMock()
    mock_driver_class.return_value = mock_driver
    mock_session = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    
    queries = CrimeQueries("bolt://localhost:7687", "neo4j", "password")
    
    # Test get_total_crimes
    mock_result = MagicMock()
    mock_record = MagicMock()
    mock_record.data.return_value = {'total_crimes': 5000}
    mock_result.__iter__.return_value = [mock_record]
    mock_session.run.return_value = mock_result
    
    assert queries.get_total_crimes() == 5000
    queries.close()

@patch("knowledge_graph.queries.query_runner.GraphDatabase.driver")
def test_geographic_queries_with_param(mock_driver_class):
    mock_driver = MagicMock()
    mock_driver_class.return_value = mock_driver
    mock_session = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    
    queries = GeographicQueries("bolt://localhost:7687", "neo4j", "password")
    
    mock_result = MagicMock()
    mock_record = MagicMock()
    mock_record.data.return_value = {'crime_count': 150}
    mock_result.__iter__.return_value = [mock_record]
    mock_session.run.return_value = mock_result
    
    assert queries.get_crimes_by_district("12") == 150
    # ensure parameter was passed
    mock_session.run.assert_called()
    queries.close()
