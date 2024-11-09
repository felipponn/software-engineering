import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decimal import Decimal

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from utils.connect_db import execute_query, execute_query_fetchone, execute_query_fetchall
from backend.product import Product

class TestProduct(unittest.TestCase):

    @patch('backend.product.execute_query_fetchall')
    def test_get_products(self, mock_execute_query_fetchall):
        # Mocking the database return value for product IDs
        mock_execute_query_fetchall.return_value = [
            (1,),
            (2,),
            (3,)
        ]

        # Call the static method to fetch products
        products = Product.get_products()

        # Assert that the return is a list of product IDs
        self.assertIsInstance(products, list)
        self.assertEqual(len(products), 3)

        # Assert the values of the product IDs
        self.assertEqual(products[0], 1)
        self.assertEqual(products[1], 2)
        self.assertEqual(products[2], 3)

    @patch('backend.product.execute_query_fetchall')
    def test_get_products_no_data(self, mock_execute_query_fetchall):
        # Simulate no products in the database
        mock_execute_query_fetchall.return_value = []

        # Call the static method to fetch products
        products = Product.get_products()

        # Assert that the return is an empty list
        self.assertIsInstance(products, list)
        self.assertEqual(len(products), 0)

    @patch('backend.product.execute_query_fetchone')
    @patch('backend.product.execute_query_fetchall')
    def test_get_profile(self, mock_execute_query_fetchall, mock_execute_query_fetchone):
        # Mocking the database return value for a product profile
        mock_execute_query_fetchone.return_value = (
            1, 'Coke', "Refreshing soda", Decimal('1.50')
        )
        mock_execute_query_fetchall.return_value = [
            (1, "Av. Paulista, 1000"),
            (2, "Av. Paulista, 1000"),
            (3, "Av. Paulista, 1500")
        ]

        # Create a Product object with product_id 1
        product = Product(1)

        # Call the method to fetch the product profile
        profile = product.get_profile()

        # Assert that the profile matches the expected data
        self.assertEqual(profile[0]['product_id'], 1)
        self.assertEqual(profile[0]['name'], 'Coke')
        self.assertEqual(profile[0]['description'], 'Refreshing soda')
        self.assertEqual(profile[0]['price'], Decimal('1.50'))
        
        # Assert that the available machines are as expected
        self.assertIsInstance(profile[1], list)
        self.assertEqual(len(profile[1]), 3)
        self.assertEqual(profile[1][0][0], 1)
        self.assertEqual(profile[1][0][1], "Av. Paulista, 1000")
        self.assertEqual(profile[1][1][0], 2)
        self.assertEqual(profile[1][1][1], "Av. Paulista, 1000")
        self.assertEqual(profile[1][2][0], 3)
        self.assertEqual(profile[1][2][1], "Av. Paulista, 1500")

if __name__ == '__main__':
    unittest.main()
