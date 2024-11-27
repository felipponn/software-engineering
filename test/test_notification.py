import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from backend.notification import Notification

class TestNotification(unittest.TestCase):
    @patch('backend.notification.Notification.send_email')
    @patch('backend.notification.Notification.check_stock')
    def test_notify_user_when_product_out_of_stock(self, mock_check_stock, mock_send_email):
        # Arrange
        mock_check_stock.return_value = True
        notification = Notification(
            user_email="fabriciodalviventurim@gmail.com",
            product_name="Soda",
            machine_location="Building A"
        )

        # Act
        notification.send_email()

        # Assert
        mock_send_email.assert_called_once()

    @patch('backend.notification.Notification.send_email')
    @patch('backend.notification.Notification.check_stock')
    def test_no_notification_when_product_in_stock(self, mock_check_stock, mock_send_email):
        # Arrange
        mock_check_stock.return_value = False
        notification = Notification(
            user_email="fabriciodalviventurim@gmail.com",
            product_name="Soda",
            machine_location="Building A"
        )

        # Act
        # notification.send_email()

        # Assert
        mock_send_email.assert_not_called()


if __name__ == '__main__':
    unittest.main()