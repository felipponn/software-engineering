import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from backend.manager import Manager

class TestManager(unittest.TestCase):
    @patch('backend.manager.execute_query')
    def test_view_all_issues_no_filters(self, mock_execute_query):
        """
        Test view_all_issues with no filters (should return all issues).
        """
        manager = Manager(user_name="John Doe", email="john.doe@example.com", password="password123", phone="1234567890")
        
        # Mock the data returned by execute_query
        mock_execute_query.return_value = [
            ('report-uuid-1', 'user-uuid-1', 'machine-uuid-1', 'Machine', 'Broken Machine', 'The coffee machine is not dispensing coffee.', 'reported', '2024-10-12 10:20:00', None),
            ('report-uuid-2', 'user-uuid-2', None, 'App', 'App Bug', 'The app crashes when submitting a report.', 'in progress', '2024-10-11 14:35:00', None),
        ]
        
        # Call the method
        result = manager.view_all_issues()

        # Assert the result
        expected_result = [
            {
                'report_id': 'report-uuid-1',
                'user_id': 'user-uuid-1',
                'machine_id': 'machine-uuid-1',
                'report_target': 'Machine',
                'issue_type': 'Broken Machine',
                'description': 'The coffee machine is not dispensing coffee.',
                'status': 'reported',
                'created_at': '2024-10-12 10:20:00',
                'resolved_at': None
            },
            {
                'report_id': 'report-uuid-2',
                'user_id': 'user-uuid-2',
                'machine_id': None,
                'report_target': 'App',
                'issue_type': 'App Bug',
                'description': 'The app crashes when submitting a report.',
                'status': 'in progress',
                'created_at': '2024-10-11 14:35:00',
                'resolved_at': None
            }
        ]
        self.assertEqual(result, expected_result)

    @patch('backend.manager.execute_query')
    def test_view_all_issues_with_filters(self, mock_execute_query):
        """
        Test view_all_issues with specific filters (issue type and user_id).
        """
        
        manager = Manager(user_name="John Doe", email="john.doe@example.com", password="password123", phone="1234567890")
        
        # Mock the data returned by execute_query
        mock_execute_query.return_value = [
            ('report-uuid-3', 'user-uuid-1', 'machine-uuid-2', 'Machine', 'Out of Coffee', 'The machine is out of coffee.', 'reported', '2024-10-15 09:30:00', None),
        ]
        
        # Call the method with filters
        result = manager.view_all_issues(type="Out of Coffee")

        # Assert the result
        expected_result = [
            {
                'report_id': 'report-uuid-3',
                'user_id': 'user-uuid-1',
                'machine_id': 'machine-uuid-2',
                'report_target': 'Machine',
                'issue_type': 'Out of Coffee',
                'description': 'The machine is out of coffee.',
                'status': 'reported',
                'created_at': '2024-10-15 09:30:00',
                'resolved_at': None
            }
        ]
        self.assertEqual(result, expected_result)

    @patch('backend.manager.execute_query')
    def test_view_all_issues_no_results(self, mock_execute_query):
        """
        Test view_all_issues when no issues match the filters.
        """
        manager = Manager(user_name="John Doe", email="john.doe@example.com", password="password123", phone="1234567890")
        
        # Mock the data returned by execute_query (empty list, no issues found)
        mock_execute_query.return_value = []

        # Call the method with filters that result in no matches
        result = manager.view_all_issues(type="Nonexistent Issue")

        # Assert that the result is an empty list
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
