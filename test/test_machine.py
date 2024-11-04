import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from backend.machine import Machine

class TestMachine(unittest.TestCase):

    @patch('backend.machine.execute_query_fetchall')
    def test_get_machines(self, mock_execute_query_fetchall):
        # Mocking the database return value for machine IDs
        mock_execute_query_fetchall.return_value = [
            (1,), (2,), (3,)
        ]

        # Call the static method to fetch machines
        machines = Machine.get_machines()

        # Assert that the return is a list of machine IDs
        self.assertIsInstance(machines, list)
        self.assertEqual(len(machines), 3)

        # Assert the values of the machine IDs
        self.assertEqual(machines[0][0], 1)
        self.assertEqual(machines[1][0], 2)
        self.assertEqual(machines[2][0], 3)

    @patch('backend.machine.execute_query_fetchall')
    def test_get_machines_no_data(self, mock_execute_query_fetchall):
        # Simulate no machines in the database
        mock_execute_query_fetchall.return_value = []

        # Call the static method to fetch machines
        machines = Machine.get_machines()

        # Assert that the return is an empty list
        self.assertIsInstance(machines, list)
        self.assertEqual(len(machines), 0)

    @patch('backend.machine.execute_query_fetchone')
    def test_get_profile(self, mock_execute_query_fetchone):
        # Mocking the database return value for a machine profile
        mock_execute_query_fetchone.return_value = (
            1, 'Building A - Lobby', 'operational', datetime(2024, 9, 1), datetime(2023, 1, 15)
        )

        # Instantiate a Machine object with a specific ID
        machine = Machine(
            machine_id=1
        )

        # Call the method to get the machine profile
        profile = machine.get_profile()

        # Assert that the profile matches the expected data
        self.assertEqual(profile[0], 1)
        self.assertEqual(profile[1], 'Building A - Lobby')
        self.assertEqual(profile[2], 'operational')
        self.assertEqual(profile[3], datetime(2024, 9, 1))
        self.assertEqual(profile[4], datetime(2023, 1, 15))

    @patch('backend.machine.execute_query_fetchone')
    def test_get_profile_no_data(self, mock_execute_query_fetchone):
        # Simulate no data found for the machine ID
        mock_execute_query_fetchone.return_value = None

        # Instantiate a Machine object with a specific ID
        machine = Machine(
            machine_id=999  # Assuming this ID does not exist
        )

        # Call the method to get the machine profile
        profile = machine.get_profile()

        # Assert that the profile is None (indicating no data found)
        self.assertIsNone(profile)

if __name__ == '__main__':
    unittest.main()
