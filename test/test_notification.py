import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from backend.notification import Notification

class TestNotification(unittest.TestCase):

    @patch('backend.notification.send_email')
    def test_notify_user_when_product_out_of_stock(self, mock_send_email):
        # Arrange
        notification = Notification()
        user_email = "fabriciodalviventurim@gmail.com"
        product_name = "Soda"
        vending_machine_location = "Building A"

        # Act
        notification.notify_user_out_of_stock(user_email, product_name, vending_machine_location)

        # Assert
        mock_send_email.assert_called_once_with(
            user_email,
            f"Product {product_name} is out of stock",
            f"The product {product_name} is out of stock in the vending machine located at {vending_machine_location}. Please check another location."
        )

    @patch('backend.notification.send_email')
    def test_no_notification_when_product_in_stock(self, mock_send_email):
        # Arrange
        notification = Notification()
        user_email = "fabriciodalviventurim@gmail.com"
        product_name = "Soda"
        vending_machine_location = "Building A"

        # Act
        notification.notify_user_in_stock(user_email, product_name, vending_machine_location)

        # Assert
        mock_send_email.assert_not_called()

if __name__ == '__main__':
    unittest.main()