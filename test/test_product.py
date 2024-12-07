import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decimal import Decimal

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from utils.connect_db import Database
from backend.product import Product

class TestProduct(unittest.TestCase):

    # @patch('utils.connect_db.Database.execute_query_fetchall')
    # def test_get_products(self, mock_execute_query_fetchall):
    #     # Mocking the database return value for product IDs
    #     mock_execute_query_fetchall.return_value = [
    #         (1,),
    #         (2,),
    #         (3,)
    #     ]

    #     # Call the static method to fetch products
    #     products = Product.get_products()

    #     # Assert that the return is a list of product IDs
    #     self.assertIsInstance(products, list)
    #     self.assertEqual(len(products), 3)

    #     # Assert the values of the product IDs
    #     self.assertEqual(products[0][0], 1)
    #     self.assertEqual(products[1][0], 2)
    #     self.assertEqual(products[2][0], 3)

    # @patch('utils.connect_db.Database.execute_query_fetchall')
    # def test_get_products_no_data(self, mock_execute_query_fetchall):
    #     # Simulate no products in the database
    #     mock_execute_query_fetchall.return_value = []

    #     # Call the static method to fetch products
    #     products = Product.get_products()

    #     # Assert that the return is an empty list
    #     self.assertIsInstance(products, list)
    #     self.assertEqual(len(products), 0)

    # @patch('utils.connect_db.Database.execute_query_fetchone')
    # @patch('utils.connect_db.Database.execute_query_fetchall')
    # @patch('utils.connect_db.Database.execute_query_fetchall')
    # def test_get_profile(self, mock_execute_query_fetchall_1, mock_execute_query_fetchall_2, mock_execute_query_fetchone):
    #     # Mocking the database return value for a product profile
    #     mock_execute_query_fetchone.return_value = (
    #         1, 'Coke', "Refreshing soda", Decimal('1.50')
    #     )
    #     mock_execute_query_fetchall_1.return_value = [
    #         (1, "Av. Paulista, 1000"),
    #         (2, "Av. Paulista, 1000"),
    #         (3, "Av. Paulista, 1500")
    #     ]
    #     mock_execute_query_fetchall_2.return_value = [
    #         (1, "Alice Smith", 4, "So refreshing!", datetime(2024, 4, 1)),
    #         (2, "Bob Johnson", 3, "Could be better...", datetime(2021, 1, 15)),
    #         (3, "John Bobson", 2, "", datetime(2023, 9, 1))
    #     ]

    #     # Create a Product object with product_id 1
    #     product = Product(1)

    #     # Call the method to fetch the product profile
    #     profile = product.get_profile()

    #     # Assert that the profile matches the expected data
    #     self.assertEqual(profile[0]['product_id'], 1)
    #     self.assertEqual(profile[0]['name'], 'Coke')
    #     self.assertEqual(profile[0]['description'], 'Refreshing soda')
    #     self.assertEqual(profile[0]['price'], Decimal('1.50'))
        
    @patch('utils.connect_db.Database.execute_query_fetchone')
    @patch('utils.connect_db.Database.execute_query_fetchall')
    def test_get_profile_with_reviews(self, mock_execute_query_fetchall, mock_execute_query_fetchone):
        # Mocking the database return value for a product profile
        mock_execute_query_fetchone.return_value = (
            1, 'Coke', "Refreshing soda", Decimal('1.50')
        )
        mock_execute_query_fetchall.side_effect = [
            [
                (1, "Av. Paulista", 1000),
                (2, "Av. Paulista", 1000),
                (3, "Av. Paulista", 1500)
            ],
            [
                (1, "Alice Smith", 4, "So refreshing!", datetime(2024, 4, 1)),
                (2, "Bob Johnson", 3, "Could be better...", datetime(2021, 1, 15)),
                (3, "John Bobson", 2, "", datetime(2023, 9, 1))
            ]
        ]

        # Create a Product object with product_id 1
        product = Product(1)
        profile = product.get_profile()

        # Assert that the profile matches the expected data
        self.assertEqual(profile[0]['product_id'], 1)
        self.assertEqual(profile[0]['name'], 'Coke')
        self.assertEqual(profile[0]['description'], 'Refreshing soda')
        self.assertEqual(profile[0]['price'], Decimal('1.50'))

        # Assert that the available machines are as expected
        self.assertIsInstance(profile[1], list)
        self.assertEqual(len(profile[1]), 3)
        self.assertEqual(profile[1][0]['machine_id'], 1)
        self.assertEqual(profile[1][0]['location'], "Av. Paulista")
        self.assertEqual(profile[1][0]['quantity'], 1000)
        self.assertEqual(profile[1][1]['machine_id'], 2)
        self.assertEqual(profile[1][1]['location'], "Av. Paulista")
        self.assertEqual(profile[1][1]['quantity'], 1000)
        self.assertEqual(profile[1][2]['machine_id'], 3)
        self.assertEqual(profile[1][2]['location'], "Av. Paulista")
        self.assertEqual(profile[1][2]['quantity'], 1500)

        # Assert that the reviews are as expected
        self.assertIsInstance(profile[2], dict)
        self.assertEqual(len(profile[2]), 5)
        self.assertEqual(profile[2]['mean_rating'], 3)
        self.assertEqual(profile[2]['count_reviews'], 3)
        self.assertEqual(profile[2]['most_recent'], datetime(2024, 4, 1))
        self.assertEqual(profile[2]['num_filtered_reviews'], 2)
        self.assertIsInstance(profile[2]['reviews'], list)
        self.assertEqual(len(profile[2]['reviews']), 2)

    # def test_post_process_reviews(self):
    #     # Prepare mock reviews
    #     reviews = [
    #         (1, "Alice Smith", 4, "So refreshing!", datetime(2024, 4, 1)),
    #         (2, "Bob Johnson", 3, "Could be better...", datetime(2021, 1, 15)),
    #         (3, "John Bobson", 2, "", datetime(2023, 9, 1))
    #     ]

    #     processed_reviews = Product.post_process_reviews(reviews)
    #     # Check the processed reviews
    #     self.assertEqual(processed_reviews['mean_rating'], 3)
    #     self.assertEqual(processed_reviews['count_reviews'], 3)
    #     self.assertEqual(processed_reviews['most_recent'], datetime(2024, 4, 1))
    #     self.assertEqual(processed_reviews['num_filtered_reviews'], 2)
    #     self.assertIsInstance(processed_reviews['reviews'], list)
    #     self.assertEqual(len(processed_reviews['reviews']), 2)

if __name__ == '__main__':
    unittest.main()
