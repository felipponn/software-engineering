import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from backend.user import User


class TestUser(unittest.TestCase):

    @patch('backend.user.execute_query_fetchone')
    def test_save_db(self, mock_fetchone):
        # Setup the mock
        mock_fetchone.return_value = ['mock-user-id']

        # Create a user
        user = User('test_name', 'test_password', 'test_email@example.com', '1234567890')
        
        # Call save_db
        user.save_db()

        # Check if user_id was set correctly
        self.assertEqual(user.user_id, 'mock-user-id')

        # Assert execute_query_fetchone was called with the correct parameters
        expected_query = (
                """
                INSERT INTO Users (name, email, phone_number, password, role)
                VALUES (%s, '%s', '%s', '%s' ,'customer')
                RETURNING user_id;
                """
        )

        mock_fetchone.assert_called_once_with(expected_query, 
            ('test_name', 'test_email@example.com', '1234567890', 'test_password'), True)


    @patch('backend.user.execute_query_fetchone')
    def test_authenticate_success(self, mock_fetchone):
        # Setup the mock
        mock_fetchone.return_value = ['mock-user-id', 'test_name', 'test_email@example.com', 'hashed_password', '1234567890']

        # Call the authenticate method
        user = User.authenticate('test_email@example.com', 'hashed_password')

        # Assert a User object is returned
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'test_email@example.com')

    @patch('backend.user.execute_query_fetchone')
    def test_authenticate_fail_wrong_password(self, mock_fetchone):
        # Setup the mock
        mock_fetchone.return_value = ['mock-user-id', 'test_name', 'test_email@example.com', 'hashed_password', '1234567890']

        # Call the authenticate method with the wrong password
        user = User.authenticate('test_email@example.com', 'wrong_password')

        # Assert no user object is returned
        self.assertIsNone(user)

    @patch('backend.user.execute_query')
    def test_report(self, mock_execute_query):
        # Create a user and assign a mock user_id
        user = User('test_name', 'test_password', 'test_email@example.com', '1234567890', user_id='mock-user-id')

        # Call report method
        user.report(target='Machine', type='Broken Machine', machine_id='mock-machine-id', message='Machine not working.')

        # Assert execute_query was called with the correct parameters
        mock_execute_query.assert_called_once_with(
                """
                INSERT INTO User_Reports (user_id, machine_id, report_target, issue_type, description)
                VALUES (%s, %s, %s, %s, %s)
                """,
            ('mock-user-id', 'mock-machine-id', 'Machine', 'Broken Machine', 'Machine not working.')
        )

if __name__ == '__main__':
    unittest.main()
