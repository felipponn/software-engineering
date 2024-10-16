import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from backend.machine import Machine

class TestMachine(unittest.TestCase):

    @patch('backend.machine.execute_query_fetchall')
    def test_get_machines(self, mock_execute_query_fetchall):
        # Mocking the database return value
        mock_execute_query_fetchall.return_value = [
            (1, 'Building A - Lobby', 'operational', '2024-09-01', '2023-01-15'),
            (2, 'Building B - Kitchen', 'under maintenance', '2024-10-01', '2022-07-20')
        ]

        # Call the static method to fetch machines
        machines = Machine.get_machines()

        # Assert that the return is a list of Machine objects
        self.assertIsInstance(machines, list)
        self.assertEqual(len(machines), 2)

        # Assert the properties of the first machine
        machine1 = machines[0]
        self.assertEqual(machine1.machine_id, 1)
        self.assertEqual(machine1.location, 'Building A - Lobby')
        self.assertEqual(machine1.status, 'operational')
        self.assertEqual(machine1.last_serviced_at, '2024-09-01')
        self.assertEqual(machine1.installed_at, '2023-01-15')

        # Assert the properties of the second machine
        machine2 = machines[1]
        self.assertEqual(machine2.machine_id, 2)
        self.assertEqual(machine2.location, 'Building B - Kitchen')
        self.assertEqual(machine2.status, 'under maintenance')
        self.assertEqual(machine2.last_serviced_at, '2024-10-01')
        self.assertEqual(machine2.installed_at, '2022-07-20')

    @patch('backend.machine.execute_query_fetchall')
    def test_get_machines_no_data(self, mock_execute_query_fetchall):
        # Simulate no machines in the database
        mock_execute_query_fetchall.return_value = []

        # Call the static method to fetch machines
        machines = Machine.get_machines()

        # Assert that the return is an empty list
        self.assertIsInstance(machines, list)
        self.assertEqual(len(machines), 0)

if __name__ == '__main__':
    unittest.main()
