import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from utils.connect_db import execute_query, execute_query_fetchone, execute_query_fetchall

class TestDBUtils(unittest.TestCase):

    @patch('psycopg2.connect')
    def test_execute_query(self, mock_connect):
        # Create mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Call execute_query
        query = "INSERT INTO test_table (col1) VALUES (%s)"
        execute_query(query, ('test_value',))

        # Assert that cursor.execute was called with the correct arguments
        mock_cursor.execute.assert_called_once_with(query, ('test_value',))
        mock_conn.commit.assert_called_once()

        # Assert connection and cursor are closed
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('psycopg2.connect')
    def test_execute_query_fetchone(self, mock_connect):
        # Create mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock fetchone() response
        mock_cursor.fetchone.return_value = ('test_row',)

        # Call execute_query_fetchone
        query = "SELECT * FROM test_table WHERE col1 = %s"
        result = execute_query_fetchone(query, ('test_value',))

        # Assert that cursor.execute was called with the correct arguments
        mock_cursor.execute.assert_called_once_with(query, ('test_value',))
        self.assertEqual(result, ('test_row',))

        # Assert connection and cursor are closed
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('psycopg2.connect')
    def test_execute_query_fetchall(self, mock_connect):
        # Create mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock fetchall() response
        mock_cursor.fetchall.return_value = [('row1',), ('row2',)]

        # Call execute_query_fetchall
        query = "SELECT * FROM test_table"
        result = execute_query_fetchall(query, ())

        # Assert that cursor.execute was called with the correct arguments
        mock_cursor.execute.assert_called_once_with(query, ())
        self.assertEqual(result, [('row1',), ('row2',)])

        # Assert connection and cursor are closed
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
