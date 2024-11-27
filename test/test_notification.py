import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from backend.notification import Notification, EmailSender

class TestNotification(unittest.TestCase):

    @patch.object(EmailSender, 'send_email')
    def test_notify_user_when_product_out_of_stock(self, mock_send_email):
        # Arrange
        notification = Notification()
        user_email = "gabrielpereirajp1201@gmail.com"
        product_name = "Soda"
        vending_machine_location = "Building A"

        # Act
        notification.subscribe(user_email)
        notification.notify(f"Product {product_name} is out of stock", 
                            f"The product {product_name} is out of stock in the vending machine located at {vending_machine_location}. Please check another location.")

        # Assert
        mock_send_email.assert_called_once_with(
            user_email,
            f"Product {product_name} is out of stock",
            f"The product {product_name} is out of stock in the vending machine located at {vending_machine_location}. Please check another location."
        )

    @patch.object(EmailSender, 'send_email')
    def test_no_notification_when_product_in_stock(self, mock_send_email):
        # Arrange
        notification = Notification()
        user_email = "gabrielpereirajp1201@gmail.com"
        product_name = "Soda"
        vending_machine_location = "Building A"

        # Act
        notification.subscribe(user_email)
        # No notification should be sent in this case
        notification.notify("Product in stock", "The product is in stock.")

        # Assert
        mock_send_email.assert_called_once_with(
            user_email,
            "Product in stock",
            "The product is in stock."
        )

if __name__ == '__main__':
    unittest.main()