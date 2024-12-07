import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decimal import Decimal

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from utils.connect_db import Database
from backend.machine import Machine

class TestMachine(unittest.TestCase):

    @patch('utils.connect_db.Database.execute_query_fetchall')
    def test_get_machines(self, mock_execute_query_fetchall):
        # Mocking the database return value for machine IDs
        mock_execute_query_fetchall.return_value = [
            (1,),
            (2,),
            (3,)
        ]

        # Call the static method to fetch machines
        machines = Machine.get_machines()

        # Assert that the return is a list of machine IDs
        self.assertIsInstance(machines, list)
        self.assertEqual(len(machines), 3)

        # Assert the values of the machine IDs
        self.assertEqual(machines[0], 1)
        self.assertEqual(machines[1], 2)
        self.assertEqual(machines[2], 3)
        
    @patch('utils.connect_db.Database.execute_query_fetchall')
    def test_get_machines_no_data(self, mock_execute_query_fetchall):
        # Simulate no machines in the database
        mock_execute_query_fetchall.return_value = []

        # Call the static method to fetch machines
        machines = Machine.get_machines()

        # Assert that the return is an empty list
        self.assertIsInstance(machines, list)
        self.assertEqual(len(machines), 0)

    @patch('utils.connect_db.Database.execute_query_fetchone')
    @patch('utils.connect_db.Database.execute_query_fetchall')
    @patch('utils.connect_db.Database.execute_query_fetchall')
    def test_get_profile(self, mock_execute_query_fetchall_1, mock_execute_query_fetchall_2, mock_execute_query_fetchone):
        # Mocking the database return value for a machine profile
        mock_execute_query_fetchone.return_value = (
            1, 'Building A - Lobby', 'operational', datetime(2024, 9, 1), datetime(2023, 1, 15)
        )
        mock_execute_query_fetchall_1.return_value = [
            ('Espresso', Decimal('2.50')),
            ('Cappuccino', Decimal('3.00'))
        ]
        mock_execute_query_fetchall_2.return_value = [
            (1, 'Alice Smith', 4, 'Great machine!', datetime.now()),
            (2, 'Bob Johnson', 5, 'Best coffee ever!', datetime.now()),
            (3, 'Charlie Brown', 3, None, datetime.now()),
        ]

        # Instantiate a Machine object with a specific ID
        machine = Machine(
            machine_id=1
        )

        # Call the method to get the machine profile
        profile = machine.get_profile()

        # Assert that the profile matches the expected data
        self.assertEqual(profile[0]['machine_id'], 1)
        self.assertEqual(profile[0]['location'], 'Building A - Lobby')
        self.assertEqual(profile[0]['status'], 'operational')
        self.assertEqual(profile[0]['last_maintenance'], datetime(2024, 9, 1))
        self.assertEqual(profile[0]['installation_date'], datetime(2023, 1, 15))

    @patch('utils.connect_db.Database.execute_query_fetchone')
    @patch('utils.connect_db.Database.execute_query_fetchall')
    def test_get_profile(self, mock_execute_query_fetchall, mock_execute_query_fetchone):
        # Mocking the database return value for a machine profile
        mock_execute_query_fetchone.return_value = (
            1, 'Building A - Lobby', 'operational', datetime(2024, 9, 1), datetime(2023, 1, 15)
        )
        mock_execute_query_fetchall.side_effect = [
            [
                ('Espresso', Decimal('2.50'), 1, 10),
                ('Cappuccino', Decimal('3.00'), 2, 5)
            ],
            [
                (1, 'Alice Smith', 4, 'Great machine!', datetime.now()),
                (2, 'Bob Johnson', 5, 'Best coffee ever!', datetime.now()),
                (3, 'Charlie Brown', 3, None, datetime.now()),
            ]
        ]

        machine = Machine(machine_id=1)
        profile, available_products, reviews_info = machine.get_profile()

        # Adjust the expected profile output to match the mocked return value
        expected_profile = {
            'machine_id': 1,
            'location': 'Building A - Lobby',
            'status': 'operational',
            'last_maintenance': '2024-09-01',
            'installation_date': '2023-01-15'
        }
        
        # Check if the profile matches
        self.assertEqual(profile, expected_profile)
        # Check if available products are as expected
        self.assertEqual(available_products, [{'name': 'Espresso', 'price': '2.50', 'product_id': 1, 'quantity': 10}, {'name': 'Cappuccino', 'price': '3.00', 'product_id': 2, 'quantity': 5}])
        
        # Check if reviews_info is processed correctly
        self.assertEqual(reviews_info['mean_rating'], 4)  # Mean of 3, 4 e 5
        self.assertEqual(reviews_info['count_reviews'], 3)  # Total reviews
        self.assertEqual(reviews_info['num_filtered_reviews'], 2)  # Reviews with comments

    def test_post_process_reviews(self):
        # Prepare mock reviews
        reviews = [
            (1, 'Alice Smith', 4, 'Great machine!', datetime.now()),
            (2, 'Bob Johnson', 5, 'Best coffee ever!', datetime.now()),
            (3, 'Charlie Brown', 3, None, datetime.now()),  # Review without comment
        ]

        processed_data = Machine.post_process_reviews(reviews)
        # Check mean rating calculation
        self.assertEqual(processed_data['mean_rating'], 4.0)  # Mean of 4, 5, and 3
        self.assertEqual(processed_data['count_reviews'], 3)  # Total reviews
        self.assertEqual(processed_data['num_filtered_reviews'], 2)  # Reviews with comments
        self.assertEqual(len(processed_data['reviews']), 2)  # Filtered reviews count

if __name__ == '__main__':
    unittest.main()
