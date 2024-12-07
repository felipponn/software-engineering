import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock

class TestNotification(unittest.TestCase):
    def test_notify_user_when_product_out_of_stock(self, mock_check_stock, mock_send_email):
        pass
    
    def test_no_notification_when_product_in_stock(self, mock_check_stock, mock_send_email):
        pass
    
if __name__ == '__main__':
    unittest.main()