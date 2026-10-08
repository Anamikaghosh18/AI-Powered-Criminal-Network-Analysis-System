import pytest
from unittest.mock import patch, MagicMock
from knowledge_graph.validation.graph_validator import GraphValidator

@patch("knowledge_graph.validation.graph_validator.GraphDatabase.driver")
def test_validation_connectivity(mock_driver_class):
    mock_driver = MagicMock()
    mock_driver_class.return_value = mock_driver
    
    validator = GraphValidator("bolt://localhost:7687", "neo4j", "password")
    
    # Setup mock returns for a PASS scenario
    mock_session = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    
    # Mocking run_query internally to return empty lists for issues
    with patch.object(validator, 'run_query') as mock_run_query:
        def side_effect(query):
            if "total_nodes" in query.lower():
                return [{'total_nodes': 100}]
            elif "relationshiptype" in query.lower():
                return [{'relationshipType': 'HAS_TYPE', 'count': 100}]
            elif "earliest" in query.lower():
                return [{'earliest': '2001', 'latest': '2026'}]
            elif "missing_case" in query.lower():
                return [{'total': 100, 'missing_case': 0, 'missing_year': 0, 'missing_arrest': 0}]
            elif "invalid_lat" in query.lower():
                return [{'total': 100, 'missing_coords': 0, 'invalid_lat': 0, 'invalid_lon': 0}]
            elif "count(c) as count" in query.lower():
                return [{'count': 0}]
            return [{'label': 'Crime', 'count': 100}] # Default mock fallback
            
        mock_run_query.side_effect = side_effect
        
        report = validator.validate()
        
        assert "Status: PASS" in report
        assert "FINAL STATUS\n========================================\nPASS" in report
        
    validator.close()
    mock_driver.close.assert_called_once()
