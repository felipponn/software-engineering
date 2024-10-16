import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from backend.machine import Machine


class TestMachine(unittest.TestCase):

    @patch('backend.machine.execute_query_fetchone')
    def test_save_db(self, mock_fetchone):
        # Setup the mock
        mock_fetchone.return_value = ['mock-machine-id']

        # Create a machine
        machine = Machine(
            machine_id=None,  # ID is set after saving to the database
            location="Café do Prédio Principal",
            status="operational",
            last_serviced_at='2024-09-01',
            installed_at='2023-01-15'
        )
        
        # Call save_db
        machine.save_db()

        # Check if machine_id was set correctly
        self.assertEqual(machine.machine_id, 'mock-machine-id')

        # Assert execute_query_fetchone was called with the correct parameters
        expected_query = (
            """
            INSERT INTO Machines (location, status, last_serviced_at, installed_at)
            VALUES (%s, %s, %s, %s)
            RETURNING machine_id;
            """
        )
        mock_fetchone.assert_called_once_with(
            expected_query,
            ('Café do Prédio Principal', 'operational', '2024-09-01', '2023-01-15')
        )

    @patch('backend.machine.execute_query_fetchall')
    def test_get_machines(self, mock_fetchall):
        # Setup the mock
        mock_fetchall.return_value = [
            ('mock-machine-id-1', 'Café do Prédio Principal', 'operational', '2024-09-01', '2023-01-15'),
            ('mock-machine-id-2', 'Biblioteca', 'under maintenance', '2024-10-01', '2022-07-20')
        ]

        # Call the get_machines method
        machines = Machine.get_machines()

        # Assert the return is a list of Machine objects
        self.assertIsInstance(machines, list)
        self.assertEqual(len(machines), 2)

        # Assert the properties of the first machine
        machine1 = machines[0]
        self.assertEqual(machine1.location, 'Café do Prédio Principal')
        self.assertEqual(machine1.status, 'operational')
        self.assertEqual(machine1.last_serviced_at, '2024-09-01')
        self.assertEqual(machine1.installed_at, '2023-01-15')

        # Assert the properties of the second machine
        machine2 = machines[1]
        self.assertEqual(machine2.location, 'Biblioteca')
        self.assertEqual(machine2.status, 'under maintenance')
        self.assertEqual(machine2.last_serviced_at, '2024-10-01')
        self.assertEqual(machine2.installed_at, '2022-07-20')

if __name__ == '__main__':
    unittest.main()
